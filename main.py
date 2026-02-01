import pygame
import sys
from config import (
    WIDTH, HEIGHT, PLAYER_SIZE, ENEMY_SIZE, FPS, BASE_ATTACK_COOLDOWN, ATTACK_RADIUS,
    PLAYER_BASE_HP, REGEN_INTERVAL_MS, ENEMY_SPAWN_TIME, XP_BASE, PLAYING, GAME_OVER, LEVEL_UP
)
from entities.enemy import Enemy
from entities.attack import Attack
from upgrades.upgrades import generate_upgrade_options, apply_upgrade
from ui.buttons import get_upgrade_buttons, check_button_click
from ui.hud import draw_hud, draw_attack_radius

# --- Init ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cubitos VS")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# --- Utils ---
def reset_game():
    return {
        "player_pos": pygame.Vector2(WIDTH // 2, HEIGHT // 2),
        "enemies": [],
        "spawn_time": ENEMY_SPAWN_TIME,
        "last_spawn": pygame.time.get_ticks(),
        "last_attack": pygame.time.get_ticks(),
        "attack_line": [],
        "attack_radius": ATTACK_RADIUS,
        "start_time": pygame.time.get_ticks(),
        "end_time": None,
        "state": PLAYING,
        "xp": 0,
        "level": 1,
        "xp_needed": XP_BASE,
        "move_speed_mult": 1.0,
        "attack_speed_mult": 1.0,
        "attack_count": 1,
        "xp_mult": 1.0,
        "player_dmg": 1,
        "player_hp": PLAYER_BASE_HP,
        "player_max_hp": PLAYER_BASE_HP,
        "last_regen": pygame.time.get_ticks(),
        "regen_mult": 1.0,
        "enemy_speed_mult": 1.0,
        "spawn_time_mult": 1.0,
        "strong_enemy_enabled": False,
        "current_upgrades": []
    }

def closest_enemies(player_pos, enemies, count):
    return sorted(enemies, key=lambda e: player_pos.distance_to(e.pos))[:count]

# --- Start ---
game = reset_game()
running = True
button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 50)

# --- Main Loop ---
while running:
    clock.tick(FPS)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game["state"] == GAME_OVER and event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                game = reset_game()

        if game["state"] == LEVEL_UP and event.type == pygame.MOUSEBUTTONDOWN:
            upgrade_buttons = get_upgrade_buttons(game["current_upgrades"])
            idx = check_button_click(event.pos, upgrade_buttons)
            if idx >= 0:
                upgrade_type = game["current_upgrades"][idx][1]
                apply_upgrade(game, upgrade_type)
                game["state"] = PLAYING

    keys = pygame.key.get_pressed()

    # --- Update ---
    if game["state"] == PLAYING:
        from config import BASE_PLAYER_SPEED, MIN_SPAWN_TIME, ENEMY_ATTACK_DAMAGE, REGEN_AMOUNT
        
        move_speed = BASE_PLAYER_SPEED * game["move_speed_mult"]
        attack_cooldown = BASE_ATTACK_COOLDOWN / game["attack_speed_mult"]

        # Player movement
        if keys[pygame.K_w]:
            game["player_pos"].y -= BASE_PLAYER_SPEED
        if keys[pygame.K_s]:
            game["player_pos"].y += BASE_PLAYER_SPEED
        if keys[pygame.K_a]:
            game["player_pos"].x -= BASE_PLAYER_SPEED
        if keys[pygame.K_d]:
            game["player_pos"].x += BASE_PLAYER_SPEED

        game["player_pos"].x = max(0, min(WIDTH - PLAYER_SIZE, game["player_pos"].x))
        game["player_pos"].y = max(0, min(HEIGHT - PLAYER_SIZE, game["player_pos"].y))

        # Spawn enemies
        if now - game["last_spawn"] > game["spawn_time"] * game["spawn_time_mult"]:
            game["enemies"].append(Enemy.spawn_random(game.get("strong_enemy_enabled", False)))
            game["last_spawn"] = now
            game["spawn_time"] = max(
                MIN_SPAWN_TIME,
                int(game["spawn_time"] * 0.95)
            )

        # Enemy movement
        for enemy in game["enemies"]:
            enemy.move_towards(game["player_pos"], game["enemy_speed_mult"])

        # Attack
        if now - game["last_attack"] > attack_cooldown:
            targets = closest_enemies(
                game["player_pos"],
                game["enemies"],
                game["attack_count"]
            )
            game["attack_line"].clear()

            for target in targets:
                if game["player_pos"].distance_to(target.pos) <= ATTACK_RADIUS:
                    if target.take_damage(game["player_dmg"]):
                        game["enemies"].remove(target)
                        game["xp"] += int(target.exp * game["xp_mult"])
                    else:
                        game["attack_line"].append(
                            Attack(game["player_pos"], target.pos, now)
                        )

            if game["xp"] >= game["xp_needed"]:
                game["xp"] -= game["xp_needed"]
                game["level"] += 1
                game["xp_needed"] = XP_BASE * game["level"]
                game["current_upgrades"] = generate_upgrade_options(game["level"])
                game["state"] = LEVEL_UP

            game["last_attack"] = now

        # Collision
        player_rect = pygame.Rect(*game["player_pos"], PLAYER_SIZE, PLAYER_SIZE)
        for enemy in game["enemies"]:
            enemy_rect = pygame.Rect(enemy.pos.x, enemy.pos.y, ENEMY_SIZE, ENEMY_SIZE)
            if player_rect.colliderect(enemy_rect):
                game["player_hp"] -= ENEMY_ATTACK_DAMAGE
                enemy.pos = pygame.Vector2(WIDTH + 40, pygame.randint(0, HEIGHT))
                if game["player_hp"] <= 0:
                    game["state"] = GAME_OVER
                    game["end_time"] = now
                break

        # Regeneration
        if now - game["last_regen"] >= REGEN_INTERVAL_MS:
            regen_amount = max(1, int(REGEN_AMOUNT * game.get("regen_mult", 1.0)))
            game["player_hp"] = min(game.get("player_max_hp", PLAYER_BASE_HP), game["player_hp"] + regen_amount)
            game["last_regen"] = now

    # --- Draw ---
    screen.fill((180, 180, 180))

    if game["state"] == PLAYING:
        # Draw attack radius
        draw_attack_radius(screen, game["player_pos"])

        # Draw attack lines
        for attack in game["attack_line"]:
            attack.draw(screen, now)

        # Draw player
        pygame.draw.rect(screen, (200, 0, 0), (*game["player_pos"], PLAYER_SIZE, PLAYER_SIZE))

        # Draw enemies
        for enemy in game["enemies"]:
            pygame.draw.rect(screen, enemy.get_color(), (enemy.pos.x, enemy.pos.y, ENEMY_SIZE, ENEMY_SIZE))

        # Draw HUD
        draw_hud(screen, font, game)

    if game["state"] == LEVEL_UP:
        upgrade_buttons = get_upgrade_buttons(game["current_upgrades"])
        panel_height = 210 if len(upgrade_buttons) == 3 else 260
        pygame.draw.rect(screen, (220, 220, 220), (200, 200, 400, panel_height))
        screen.blit(font.render("ELIGE UN UPGRADE", True, (0, 0, 0)), (270, 220))
        for text, rect in upgrade_buttons:
            pygame.draw.rect(screen, (100, 100, 100), rect)
            screen.blit(font.render(text, True, (255, 255, 255)),
                        (rect.x + 20, rect.y + 10))

    if game["state"] == GAME_OVER:
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 0)
        screen.blit(font.render("GAME OVER", True, (255, 0, 0)), (WIDTH // 2 - 120, HEIGHT // 2 - 50))
        pygame.draw.rect(screen, (100, 100, 100), button_rect)
        screen.blit(font.render("Reiniciar", True, (255, 255, 255)),
                    (button_rect.x + 40, button_rect.y + 10))

    pygame.display.flip()

pygame.quit()
sys.exit()


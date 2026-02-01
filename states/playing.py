import pygame
from config import (
    WIDTH, HEIGHT, PLAYER_SIZE, ENEMY_SIZE, BASE_PLAYER_SPEED, BASE_ATTACK_COOLDOWN,
    ENEMY_SPAWN_TIME, MIN_SPAWN_TIME, ENEMY_ATTACK_DAMAGE, PLAYING, LEVEL_UP, GAME_OVER
)
from entities.enemy import Enemy
from entities.attack import Attack
from upgrades.upgrades import generate_upgrade_options


def closest_enemies(player_pos, enemies, count):
    """Retorna los enemigos más cercanos al jugador"""
    return sorted(enemies, key=lambda e: player_pos.distance_to(e.pos))[:count]


def init_playing_state(game):
    """Inicializa el estado de juego PLAYING"""
    pass


def update_playing_state(game, keys, dt):
    """Actualiza la lógica del juego durante PLAYING"""
    now = pygame.time.get_ticks()
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
            if game["player_pos"].distance_to(target.pos) <= game["attack_radius"]:
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
            game["xp_needed"] = 5 * game["level"]  # XP_BASE * game["level"]
            game["current_upgrades"] = generate_upgrade_options(game["level"])
            game["state"] = LEVEL_UP

        game["last_attack"] = now

    # Collision
    player_rect = pygame.Rect(*game["player_pos"], PLAYER_SIZE, PLAYER_SIZE)
    for enemy in game["enemies"]:
        enemy_rect = pygame.Rect(enemy.pos.x, enemy.pos.y, ENEMY_SIZE, ENEMY_SIZE)
        if player_rect.colliderect(enemy_rect):
            game["player_hp"] -= ENEMY_ATTACK_DAMAGE
            if game["player_hp"] <= 0:
                game["state"] = GAME_OVER
                game["end_time"] = now
            else:
                # Reposicionar enemigo
                enemy.pos = pygame.Vector2(WIDTH + 40, pygame.randint(0, HEIGHT))
            break

    # Regeneration
    if now - game["last_regen"] >= 2000:  # REGEN_INTERVAL_MS
        regen_amount = max(1, int(3 * game.get("regen_mult", 1.0)))  # REGEN_AMOUNT
        game["player_hp"] = min(game.get("player_max_hp", 100), game["player_hp"] + regen_amount)
        game["last_regen"] = now


def draw_playing_state(screen, font, game):
    """Dibuja todo lo necesario para el estado PLAYING"""
    from ui.hud import draw_hud, draw_attack_radius
    from config import PLAYER_SIZE, ENEMY_SIZE, ATTACK_RADIUS
    
    screen.fill((180, 180, 180))
    
    # Draw attack radius
    draw_attack_radius(screen, game["player_pos"])

    # Draw attack lines
    for attack in game["attack_line"]:
        attack.draw(screen, pygame.time.get_ticks())

    # Draw player
    pygame.draw.rect(screen, (200, 0, 0), (*game["player_pos"], PLAYER_SIZE, PLAYER_SIZE))

    # Draw enemies
    for enemy in game["enemies"]:
        pygame.draw.rect(screen, enemy.get_color(), (enemy.pos.x, enemy.pos.y, ENEMY_SIZE, ENEMY_SIZE))

    # Draw HUD
    draw_hud(screen, font, game)

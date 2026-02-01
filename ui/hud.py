import pygame
from config import (
    WIDTH, HEIGHT, PLAYER_SIZE, ATTACK_RADIUS
)


def draw_hud(screen, font, game):
    """Dibuja la interfaz de usuario (nivel, XP, HP, daño)"""
    screen.blit(font.render(f"Nivel {game['level']}", True, (0, 0, 0)), (10, 10))
    screen.blit(font.render(f"XP {game['xp']} / {game['xp_needed']}", True, (0, 0, 0)), (10, 40))
    screen.blit(font.render(f"HP {game['player_hp']} / {game['player_max_hp']}", True, (255, 0, 0)), (10, 70))
    screen.blit(font.render(f"Daño {game['player_dmg']}", True, (0, 0, 0)), (10, 100))


def draw_attack_radius(screen, player_pos):
    """Dibuja el radio de ataque del jugador"""
    pygame.draw.circle(
        screen,
        (120, 120, 120),
        (int(player_pos.x + PLAYER_SIZE // 2),
         int(player_pos.y + PLAYER_SIZE // 2)),
        ATTACK_RADIUS,
        1
    )

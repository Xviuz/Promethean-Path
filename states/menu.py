import pygame
from config import WIDTH, HEIGHT


def get_menu_buttons():
    """Retorna lista de tuplas (texto, rect, action) para el menú principal"""
    buttons = []
    buttons.append(("Jugar", pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 40, 200, 50), "play"))
    buttons.append(("Salir", pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50), "quit"))
    return buttons


def draw_menu(screen, font, buttons):
    screen.fill((150, 150, 200))
    screen.blit(font.render("PROMETHEAN PATH", True, (0, 0, 0)), (WIDTH // 2 - 130, HEIGHT // 2 - 120))
    for text, rect, _ in buttons:
        pygame.draw.rect(screen, (100, 100, 100), rect)
        screen.blit(font.render(text, True, (255, 255, 255)), (rect.x + 40, rect.y + 10))
# Menú principal: botones, navegación, perfil, tienda, records

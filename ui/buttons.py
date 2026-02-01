import pygame
from config import WIDTH, HEIGHT


def get_upgrade_buttons(upgrades):
    """Crea los rectángulos de botones para los upgrades"""
    buttons = []
    y_pos = 260
    for text, _ in upgrades:
        buttons.append((text, pygame.Rect(250, y_pos, 300, 40)))
        y_pos += 50
    return buttons


def draw_button(screen, rect, text, font, bg_color=(100, 100, 100), text_color=(255, 255, 255)):
    """Dibuja un botón en pantalla"""
    pygame.draw.rect(screen, bg_color, rect)
    screen.blit(font.render(text, True, text_color),
                (rect.x + 20, rect.y + 10))


def check_button_click(pos, buttons):
    """Comprueba si se hizo click en algún botón"""
    for idx, (_, rect) in enumerate(buttons):
        if rect.collidepoint(pos):
            return idx
    return -1

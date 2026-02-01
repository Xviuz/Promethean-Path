import pygame
from config import PLAYER_SIZE, ENEMY_SIZE, ATTACK_LINE_DURATION


class Attack:
    """Clase para gestionar ataques y efectos visuales"""
    
    def __init__(self, start_pos, end_pos, creation_time):
        self.start = start_pos.copy() if isinstance(start_pos, pygame.Vector2) else pygame.Vector2(start_pos)
        self.end = end_pos.copy() if isinstance(end_pos, pygame.Vector2) else pygame.Vector2(end_pos)
        self.creation_time = creation_time
    
    def is_active(self, current_time):
        """Comprueba si el ataque aún debería mostrarse"""
        return current_time - self.creation_time <= ATTACK_LINE_DURATION
    
    def draw(self, screen, current_time):
        """Dibuja la línea de ataque si aún está activa"""
        if self.is_active(current_time):
            pygame.draw.line(
                screen, (255, 255, 0),
                self.start + pygame.Vector2(PLAYER_SIZE // 2),
                self.end + pygame.Vector2(ENEMY_SIZE // 2),
                2
            )

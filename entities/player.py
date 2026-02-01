import pygame
from config import (
    WIDTH, HEIGHT, PLAYER_SIZE, PLAYER_BASE_HP, REGEN_AMOUNT, REGEN_INTERVAL_MS
)


class Player:
    """Clase para gestionar al jugador: stats base, multiplicadores, regeneración, movimiento, ataques"""
    
    def __init__(self, x=None, y=None):
        if x is None:
            x = WIDTH // 2
        if y is None:
            y = HEIGHT // 2
            
        self.pos = pygame.Vector2(x, y)
        
        # Base stats
        self.hp = PLAYER_BASE_HP
        self.max_hp = PLAYER_BASE_HP
        self.dmg = 1
        
        # Multipliers
        self.move_speed_mult = 1.0
        self.attack_speed_mult = 1.0
        self.xp_mult = 1.0
        self.regen_mult = 1.0
        
        # Attacks
        self.attack_count = 1
        
        # Regeneration
        self.last_regen = pygame.time.get_ticks()
    
    def update_position(self, keys, base_speed, boundaries=True):
        """Actualiza la posición del jugador basado en input de teclado"""
        if keys[pygame.K_w]:
            self.pos.y -= base_speed
        if keys[pygame.K_s]:
            self.pos.y += base_speed
        if keys[pygame.K_a]:
            self.pos.x -= base_speed
        if keys[pygame.K_d]:
            self.pos.x += base_speed
        
        if boundaries:
            self.pos.x = max(0, min(WIDTH - PLAYER_SIZE, self.pos.x))
            self.pos.y = max(0, min(HEIGHT - PLAYER_SIZE, self.pos.y))
    
    def update_regen(self, current_time):
        """Actualiza la regeneración de vida"""
        if current_time - self.last_regen >= REGEN_INTERVAL_MS:
            regen_amount = max(1, int(REGEN_AMOUNT * self.regen_mult))
            self.hp = min(self.max_hp, self.hp + regen_amount)
            self.last_regen = current_time
    
    def take_damage(self, damage):
        """Reduce la vida del jugador"""
        self.hp = max(0, self.hp - damage)
        return self.hp <= 0  # Retorna True si el jugador muere
    
    def heal(self, amount):
        """Regenera la vida del jugador"""
        self.hp = min(self.max_hp, self.hp + amount)

import pygame
import random
from config import ENEMY_SIZE, ENEMY_SPEED, SPAWN_OFFSET, WIDTH, HEIGHT, STRONG_ENEMY_CHANCE, STRONG_ENEMY_HP, XP_PER_KILL, STRONG_ENEMY_EXP_MULT


class Enemy:
    """Clase para gestionar enemigos: stats, AI básica, tipos, bosses"""
    
    def __init__(self, pos, is_strong=False):
        self.pos = pygame.Vector2(pos)
        self.is_strong = is_strong
        
        # Stats
        self.hp = STRONG_ENEMY_HP if is_strong else 2
        self.exp = int(XP_PER_KILL * STRONG_ENEMY_EXP_MULT) if is_strong else XP_PER_KILL
    
    @staticmethod
    def spawn_random(strong_enabled=False):
        """Genera un enemigo en una posición aleatoria fuera de la pantalla"""
        side = random.choice(("top", "bottom", "left", "right"))
        
        if side == "top":
            pos = pygame.Vector2(random.randint(0, WIDTH), -SPAWN_OFFSET)
        elif side == "bottom":
            pos = pygame.Vector2(random.randint(0, WIDTH), HEIGHT + SPAWN_OFFSET)
        elif side == "left":
            pos = pygame.Vector2(-SPAWN_OFFSET, random.randint(0, HEIGHT))
        else:
            pos = pygame.Vector2(WIDTH + SPAWN_OFFSET, random.randint(0, HEIGHT))
        
        # Posiblemente spawn de enemigo fuerte
        is_strong = strong_enabled and random.random() < STRONG_ENEMY_CHANCE
        return Enemy(pos, is_strong)
    
    def move_towards(self, target_pos, speed_mult=1.0):
        """Mueve el enemigo hacia una posición objetivo"""
        direction = target_pos - self.pos
        if direction.length_squared() > 0:
            enemy_speed = ENEMY_SPEED * speed_mult
            self.pos += direction.normalize() * enemy_speed
    
    def take_damage(self, damage):
        """Reduce la vida del enemigo"""
        self.hp -= damage
        return self.hp <= 0  # Retorna True si el enemigo muere
    
    def get_color(self):
        """Retorna el color del enemigo según su tipo"""
        return (80, 80, 80) if self.is_strong else (0, 0, 0)

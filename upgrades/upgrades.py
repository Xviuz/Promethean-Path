import random
from config import MAX_PERCENT_UPGRADE, XP_BASE


def generate_upgrade_options(level):
    """Genera 3 opciones de upgrade para el nivel actual"""
    all_upgrades = [
        ("+2% Vel. Movimiento", "move_speed"),
        ("+5% Vel. Ataque", "attack_speed"),
        ("+1 Ataque", "attack_count"),
        ("+1 Daño", "player_dmg"),
        ("+1 HP", "player_hp"),
        ("-5% Vel. Enemigos", "enemy_speed"),
        ("-20% Spawn Rápido", "spawn_time"),
        ("+10% Reg. Salud", "hp_regen"),
    ]
    
    # Mostrar opción de XP en nivel 2 y cada 4 niveles después
    if level >= 2 and (level - 2) % 4 == 0:
        all_upgrades.append(("+10% XP", "xp_mult"))
    
    # Seleccionar 3 opciones al azar
    return random.sample(all_upgrades, min(3, len(all_upgrades)))


def apply_upgrade(game, upgrade_type):
    """Aplica un upgrade al estado del juego"""
    if upgrade_type == "move_speed":
        game["move_speed_mult"] += MAX_PERCENT_UPGRADE
    elif upgrade_type == "attack_speed":
        game["attack_speed_mult"] += 0.05
    elif upgrade_type == "attack_count":
        game["attack_count"] += 1
        game["strong_enemy_enabled"] = True
    elif upgrade_type == "player_dmg":
        game["player_dmg"] += 1
        game["strong_enemy_enabled"] = True
    elif upgrade_type == "player_hp":
        game["player_hp"] += 10
        game["player_max_hp"] += 10
    elif upgrade_type == "hp_regen":
        game["regen_mult"] += 0.10
    elif upgrade_type == "enemy_speed":
        game["enemy_speed_mult"] -= 0.05
    elif upgrade_type == "spawn_time":
        game["spawn_time_mult"] -= 0.20
    elif upgrade_type == "xp_mult":
        game["xp_mult"] += 0.10

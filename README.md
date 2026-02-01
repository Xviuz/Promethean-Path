# Promethean Path

**Promethean Path** es un juego estilo *Vampire Survivor* hecho en Python usando `pygame`.  
Controlas a un jugador que debe sobrevivir oleadas de enemigos mientras sube de nivel, gana mejoras y acumula experiencia.

---

## Características principales

- Movimiento del jugador con WASD
- Sistema de ataques automáticos con visualización de línea hacia los enemigos
- Experiencia (XP) y niveles
- Subida de nivel con selección de upgrades:
  - Velocidad de movimiento
  - Velocidad de ataque
  - Número de ataques simultáneos
  - Daño, HP y regeneración de salud
  - Modificación de velocidad de enemigos y spawn
- Diferentes tipos de enemigos, algunos más fuertes con más HP y XP
- Pantallas de `Level Up` y `Game Over`
- Modularizado para escalabilidad futura: player, enemigos, upgrades, UI, estados, etc.

---

## Requisitos

- Python 3.9+
- `pygame`  

Instalación de pygame:

```bash
pip install pygame
```


Cómo jugar
Ejecuta main.py:

bash
Copiar código
python main.py
Usa las teclas W, A, S, D para mover al jugador.

Sobrevive el mayor tiempo posible y derrota enemigos para ganar XP.

Al subir de nivel, elige mejoras en la pantalla de Level Up.

Si tu HP llega a 0, aparecerá la pantalla de Game Over.

Estructura del proyecto
powershell
Copiar código
Promethean-Path/
├── main.py
├── config.py
├── states/         # Menú, playing, level up, game over
├── entities/       # Player, enemigos y ataques
├── upgrades/       # Stats y mejoras
├── ui/             # HUD, botones y efectos
├── data/           # Guardado de perfiles y records
├── assets/         # Sprites, imágenes y sonidos
└── utils/          # Funciones auxiliares
Futuras mejoras
Diferentes tipos de enemigos y bosses con mecánicas únicas

Sistema de items y cofres

Perfil de jugador con nombre y avatar

Menú principal completo (tienda de skins, records, configuraciones)

Estadísticas avanzadas y máximos de nivel

Guardado y ranking online

Efectos visuales y animaciones mejoradas

Autor
Xviuz – Desarrollador y diseñador del juego

import pygame

# --- CONFIGURACIÓN DE PANTALLA Y RENDER ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
FPS = 60
TILE_SIZE = 32

# Paleta de colores estilo NES Clásico
COLOR_SKY = (92, 148, 252)        # Azul cielo NES
COLOR_GROUND_BASE = (200, 76, 12)  # Marrón tierra NES
COLOR_GROUND_TOP = (0, 168, 0)     # Verde césped superior
COLOR_PIPE_GREEN = (0, 168, 0)     # Verde tubería
COLOR_PIPE_DARK = (0, 100, 0)
COLOR_BLOCK_BORDER = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_MARIO_RED = (216, 40, 0)     # Rojo Mario
COLOR_MARIO_BROWN = (136, 112, 0)  # Marrón overol clásico
COLOR_MARIO_SKIN = (252, 152, 56)  # Tono piel retro

# --- FÍSICAS DEL JUGADOR (Valores en píxeles/segundo) ---
WALK_ACCELERATION = 550.0          # Aceleración horizontal al caminar
RUN_ACCELERATION = 900.0           # Aceleración horizontal en sprint (Shift)
GROUND_FRICTION = 420.0            # Fricción natural al desacelerar en suelo
SKID_FRICTION = 950.0              # Fricción de derrape al cambiar de sentido
AIR_FRICTION = 90.0                # Resistencia mínima en el aire
MAX_WALK_SPEED = 180.0             # Velocidad horizontal máxima caminando
MAX_RUN_SPEED = 310.0              # Velocidad horizontal máxima corriendo

# Físicas de Salto Variable
GRAVITY = 1200.0                   # Gravedad constante hacia abajo
JUMP_INITIAL_VELOCITY = -410.0     # Impulso instantáneo inicial del salto
JUMP_HOLD_FORCE = -680.0           # Fuerza ascendente adicional sostenida al mantener tecla
MAX_JUMP_HOLD_TIME = 0.26          # Tiempo máximo en segundos que la tecla suma impulso
FALL_GRAVITY_MULTIPLIER = 1.35     # Gravedad reforzada cuando se cae (salto con peso real)
TERMINAL_VELOCITY = 680.0          # Velocidad máxima de caída vertical

# Dimensiones de Hitbox del Jugador Pequeño
PLAYER_WIDTH = 22
PLAYER_HEIGHT = 28
PLAYER_CROUCH_HEIGHT = 18

# --- MAPEO DE CONTROLES ---
KEYS_MOVE_LEFT = (pygame.K_a, pygame.K_LEFT)
KEYS_MOVE_RIGHT = (pygame.K_d, pygame.K_RIGHT)
KEYS_JUMP = (pygame.K_SPACE, pygame.K_w, pygame.K_UP)
KEYS_RUN = (pygame.K_LSHIFT,)
KEYS_CROUCH = (pygame.K_s, pygame.K_DOWN)
KEYS_PAUSE = (pygame.K_ESCAPE, pygame.K_p)

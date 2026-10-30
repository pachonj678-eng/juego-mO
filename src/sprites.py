import pygame
from src.settings import (
    TILE_SIZE,
    COLOR_SKY,
    COLOR_GROUND_BASE,
    COLOR_GROUND_TOP,
    COLOR_PIPE_GREEN,
    COLOR_PIPE_DARK,
    COLOR_BLOCK_BORDER,
    COLOR_WHITE,
    COLOR_BLACK,
    COLOR_MARIO_RED,
    COLOR_MARIO_BROWN,
    COLOR_MARIO_SKIN,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_CROUCH_HEIGHT
)

SUPER_MARIO_HEIGHT = 48
SUPER_MARIO_CROUCH_HEIGHT = 28


def create_ground_tile() -> pygame.Surface:
    """Genera una superficie de tile de suelo clásico estilo NES (32x32)."""
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surf.fill(COLOR_GROUND_BASE)

    pygame.draw.rect(surf, COLOR_GROUND_TOP, (0, 0, TILE_SIZE, 6))
    pygame.draw.line(surf, (0, 220, 0), (0, 0), (TILE_SIZE, 0), 1)

    highlight = (230, 110, 40)
    shadow = (140, 45, 5)
    for y in (10, 20):
        pygame.draw.line(surf, shadow, (0, y), (TILE_SIZE, y), 1)
        pygame.draw.line(surf, highlight, (0, y + 1), (TILE_SIZE, y + 1), 1)
    for x in (8, 24):
        pygame.draw.line(surf, shadow, (x, 10), (x, 20), 1)
        pygame.draw.line(surf, highlight, (x + 1, 10), (x + 1, 20), 1)

    pygame.draw.rect(surf, COLOR_BLOCK_BORDER, (0, 0, TILE_SIZE, TILE_SIZE), 1)
    return surf


def create_solid_block() -> pygame.Surface:
    """Genera un bloque sólido de plataforma elevada (32x32)."""
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surf.fill((216, 120, 48))

    pygame.draw.line(surf, (255, 180, 120), (0, 0), (TILE_SIZE - 1, 0), 2)
    pygame.draw.line(surf, (255, 180, 120), (0, 0), (0, TILE_SIZE - 1), 2)
    pygame.draw.line(surf, (120, 60, 20), (0, TILE_SIZE - 1), (TILE_SIZE - 1, TILE_SIZE - 1), 2)
    pygame.draw.line(surf, (120, 60, 20), (TILE_SIZE - 1, 0), (TILE_SIZE - 1, TILE_SIZE - 1), 2)

    pygame.draw.rect(surf, (120, 60, 20), (6, 6, 20, 20), 1)
    pygame.draw.circle(surf, (255, 180, 120), (16, 16), 3)
    return surf


def create_pipe_tile(is_top: bool = False, is_left: bool = True) -> pygame.Surface:
    """Genera partes de la tubería clásica."""
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surf.fill(COLOR_PIPE_GREEN)

    highlight = (120, 255, 120)
    shadow = COLOR_PIPE_DARK

    if is_left:
        pygame.draw.line(surf, highlight, (2, 0), (2, TILE_SIZE), 2)
        pygame.draw.line(surf, shadow, (TILE_SIZE - 3, 0), (TILE_SIZE - 3, TILE_SIZE), 3)
    else:
        pygame.draw.line(surf, highlight, (4, 0), (4, TILE_SIZE), 1)
        pygame.draw.line(surf, shadow, (TILE_SIZE - 4, 0), (TILE_SIZE - 4, TILE_SIZE), 4)

    if is_top:
        pygame.draw.line(surf, highlight, (0, 1), (TILE_SIZE, 1), 2)
        pygame.draw.line(surf, shadow, (0, TILE_SIZE - 2), (TILE_SIZE, TILE_SIZE - 2), 2)

    pygame.draw.rect(surf, COLOR_BLACK, (0, 0, TILE_SIZE, TILE_SIZE), 1)
    return surf


def create_question_block(frame: int = 0) -> pygame.Surface:
    """Genera el bloque interrogación [?] animado estilo NES (32x32)."""
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    bg_colors = [
        (252, 152, 56),
        (248, 140, 40),
        (230, 125, 30),
        (248, 140, 40),
    ]
    base_col = bg_colors[frame % len(bg_colors)]
    surf.fill(base_col)

    pygame.draw.line(surf, (255, 215, 150), (0, 0), (TILE_SIZE - 1, 0), 2)
    pygame.draw.line(surf, (255, 215, 150), (0, 0), (0, TILE_SIZE - 1), 2)
    pygame.draw.line(surf, (150, 75, 15), (0, TILE_SIZE - 1), (TILE_SIZE - 1, TILE_SIZE - 1), 2)
    pygame.draw.line(surf, (150, 75, 15), (TILE_SIZE - 1, 0), (TILE_SIZE - 1, TILE_SIZE - 1), 2)

    rivet_col = (136, 60, 10)
    for rx, ry in ((3, 3), (TILE_SIZE - 5, 3), (3, TILE_SIZE - 5), (TILE_SIZE - 5, TILE_SIZE - 5)):
        pygame.draw.rect(surf, rivet_col, (rx, ry, 2, 2))

    q_shadow = (110, 45, 10)
    q_color = (255, 255, 255) if frame % 4 != 2 else (255, 235, 180)

    pygame.draw.rect(surf, q_shadow, (11, 7, 12, 3))
    pygame.draw.rect(surf, q_shadow, (19, 9, 4, 6))
    pygame.draw.rect(surf, q_shadow, (13, 14, 6, 3))
    pygame.draw.rect(surf, q_shadow, (13, 17, 4, 3))
    pygame.draw.rect(surf, q_shadow, (13, 22, 4, 4))

    pygame.draw.rect(surf, q_color, (10, 6, 12, 3))
    pygame.draw.rect(surf, q_color, (18, 8, 4, 6))
    pygame.draw.rect(surf, q_color, (12, 13, 6, 3))
    pygame.draw.rect(surf, q_color, (12, 16, 4, 3))
    pygame.draw.rect(surf, q_color, (12, 21, 4, 4))

    pygame.draw.rect(surf, COLOR_BLACK, (0, 0, TILE_SIZE, TILE_SIZE), 1)
    return surf


def create_empty_block() -> pygame.Surface:
    """Genera el bloque usado / agotado (metálico marrón sin signo)."""
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surf.fill((168, 104, 56))

    pygame.draw.line(surf, (200, 140, 90), (0, 0), (TILE_SIZE - 1, 0), 2)
    pygame.draw.line(surf, (200, 140, 90), (0, 0), (0, TILE_SIZE - 1), 2)
    pygame.draw.line(surf, (100, 55, 25), (0, TILE_SIZE - 1), (TILE_SIZE - 1, TILE_SIZE - 1), 2)
    pygame.draw.line(surf, (100, 55, 25), (TILE_SIZE - 1, 0), (TILE_SIZE - 1, TILE_SIZE - 1), 2)

    for rx, ry in ((4, 4), (TILE_SIZE - 6, 4), (4, TILE_SIZE - 6), (TILE_SIZE - 6, TILE_SIZE - 6)):
        pygame.draw.rect(surf, (80, 40, 15), (rx, ry, 3, 3))
        pygame.draw.rect(surf, (220, 160, 110), (rx, ry, 1, 1))

    pygame.draw.rect(surf, COLOR_BLACK, (0, 0, TILE_SIZE, TILE_SIZE), 1)
    return surf


def create_brick_block() -> pygame.Surface:
    """Genera el bloque clásico de ladrillos rompibles (32x32)."""
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
    brick_main = (196, 76, 16)
    brick_light = (248, 136, 72)
    mortar_dark = (0, 0, 0)

    surf.fill(brick_main)

    rows_y = [7, 15, 23]
    for y in rows_y:
        pygame.draw.line(surf, mortar_dark, (0, y), (TILE_SIZE, y), 2)

    pygame.draw.line(surf, mortar_dark, (16, 0), (16, 7), 2)
    pygame.draw.line(surf, mortar_dark, (8, 8), (8, 15), 2)
    pygame.draw.line(surf, mortar_dark, (24, 8), (24, 15), 2)
    pygame.draw.line(surf, mortar_dark, (16, 16), (16, 23), 2)
    pygame.draw.line(surf, mortar_dark, (8, 24), (8, 31), 2)
    pygame.draw.line(surf, mortar_dark, (24, 24), (24, 31), 2)

    for y in (1, 9, 17, 25):
        pygame.draw.line(surf, brick_light, (1, y), (TILE_SIZE - 2, y), 1)

    pygame.draw.rect(surf, mortar_dark, (0, 0, TILE_SIZE, TILE_SIZE), 1)
    return surf


def create_coin_surface(frame: int = 0) -> pygame.Surface:
    """Genera superficie para moneda giratoria en 4 fases de rotación."""
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    gold = (252, 196, 0)
    gold_light = (255, 240, 120)
    gold_dark = (180, 110, 0)

    step = frame % 4
    if step == 0:
        w = 14
    elif step in (1, 3):
        w = 8
    else:
        w = 4

    x = (TILE_SIZE - w) // 2
    y = 6
    h = 20

    pygame.draw.rect(surf, gold, (x, y, w, h), border_radius=2)
    pygame.draw.line(surf, gold_light, (x + 1, y + 2), (x + 1, y + h - 3), 1)
    pygame.draw.line(surf, gold_dark, (x + w - 2, y + 2), (x + w - 2, y + h - 3), 1)
    pygame.draw.rect(surf, COLOR_BLACK, (x, y, w, h), 1, border_radius=2)

    return surf


def create_brick_debris_surface() -> pygame.Surface:
    """Genera un fragmento de ladrillo que salta en 4 partes al romperse."""
    surf = pygame.Surface((12, 12), pygame.SRCALPHA)
    surf.fill((196, 76, 16))
    pygame.draw.line(surf, (248, 136, 72), (0, 0), (11, 0), 2)
    pygame.draw.line(surf, (100, 35, 5), (0, 11), (11, 11), 2)
    pygame.draw.rect(surf, COLOR_BLACK, (0, 0, 12, 12), 1)
    return surf


def create_mushroom_surface() -> pygame.Surface:
    """Genera el ítem Champiñón Rojo clásico (24x24 px)."""
    surf = pygame.Surface((24, 24), pygame.SRCALPHA)
    red = (216, 40, 0)
    beige = (252, 216, 168)
    black = COLOR_BLACK

    # Sombrero de hongo rojo
    pygame.draw.ellipse(surf, red, (1, 1, 22, 16))
    # Lunares blancos
    pygame.draw.ellipse(surf, COLOR_WHITE, (8, 2, 8, 8))
    pygame.draw.ellipse(surf, COLOR_WHITE, (2, 8, 5, 7))
    pygame.draw.ellipse(surf, COLOR_WHITE, (17, 8, 5, 7))

    # Tallo beige
    pygame.draw.rect(surf, beige, (5, 12, 14, 11), border_radius=3)
    # Ojos negros
    pygame.draw.rect(surf, black, (7, 14, 2, 4))
    pygame.draw.rect(surf, black, (15, 14, 2, 4))

    # Contorno
    pygame.draw.rect(surf, black, (0, 0, 24, 24), 1)
    return surf


def create_fireball_surface(frame: int = 0) -> pygame.Surface:
    """Genera la bola de fuego giratoria de Mario (12x12 px)."""
    surf = pygame.Surface((12, 12), pygame.SRCALPHA)
    colors = [(252, 152, 56), (216, 40, 0), (252, 216, 0)]
    main_col = colors[frame % 3]

    pygame.draw.circle(surf, main_col, (6, 6), 5)
    pygame.draw.circle(surf, (255, 255, 255), (6, 6), 2)
    pygame.draw.circle(surf, COLOR_BLACK, (6, 6), 5, 1)
    return surf


def draw_goomba_pixels(state: str = "walk", frame: int = 0) -> pygame.Surface:
    """Dibuja al enemigo Goomba en estado caminar (24x24) o aplastado (24x10)."""
    if state == "flattened":
        surf = pygame.Surface((24, 10), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (184, 68, 0), (1, 2, 22, 7))
        pygame.draw.line(surf, COLOR_BLACK, (5, 5), (9, 5), 2)
        pygame.draw.line(surf, COLOR_BLACK, (14, 5), (18, 5), 2)
        return surf

    surf = pygame.Surface((24, 24), pygame.SRCALPHA)
    brown = (184, 68, 0)
    stem_color = (252, 216, 168)
    foot_color = (80, 20, 0)

    pygame.draw.ellipse(surf, brown, (2, 2, 20, 15))

    pygame.draw.rect(surf, COLOR_WHITE, (5, 7, 4, 6))
    pygame.draw.rect(surf, COLOR_WHITE, (15, 7, 4, 6))
    pygame.draw.rect(surf, COLOR_BLACK, (7, 8, 2, 4))
    pygame.draw.rect(surf, COLOR_BLACK, (15, 8, 2, 4))
    pygame.draw.line(surf, COLOR_BLACK, (4, 6), (9, 7), 2)
    pygame.draw.line(surf, COLOR_BLACK, (19, 6), (14, 7), 2)

    pygame.draw.rect(surf, stem_color, (6, 15, 12, 5))

    if frame % 2 == 0:
        pygame.draw.ellipse(surf, foot_color, (1, 18, 10, 6))
        pygame.draw.ellipse(surf, foot_color, (13, 19, 8, 5))
    else:
        pygame.draw.ellipse(surf, foot_color, (3, 19, 8, 5))
        pygame.draw.ellipse(surf, foot_color, (13, 18, 10, 6))

    return surf


def draw_koopa_pixels(state: str = "walk", frame: int = 0) -> pygame.Surface:
    """Dibuja al Koopa Troopa caminando (24x30) o en forma de caparazón (22x20)."""
    if "shell" in state:
        surf = pygame.Surface((22, 20), pygame.SRCALPHA)
        shell_green = (0, 184, 0)
        shell_rim = (252, 216, 168)
        pygame.draw.ellipse(surf, shell_green, (1, 1, 20, 18))
        pygame.draw.ellipse(surf, shell_rim, (2, 12, 18, 6), 2)
        pygame.draw.line(surf, COLOR_BLACK, (6, 6), (16, 6), 1)
        pygame.draw.line(surf, COLOR_BLACK, (11, 2), (11, 14), 1)
        pygame.draw.rect(surf, COLOR_BLACK, (0, 0, 22, 20), 1, border_radius=6)
        return surf

    surf = pygame.Surface((24, 30), pygame.SRCALPHA)
    green = (0, 184, 0)
    yellow = (252, 196, 0)
    rim_color = (255, 255, 255)

    pygame.draw.ellipse(surf, green, (10, 2, 12, 11))
    pygame.draw.rect(surf, yellow, (16, 8, 7, 5), border_radius=2)
    pygame.draw.rect(surf, COLOR_WHITE, (14, 4, 4, 5))
    pygame.draw.rect(surf, COLOR_BLACK, (16, 5, 2, 3))

    pygame.draw.ellipse(surf, green, (2, 11, 18, 14))
    pygame.draw.ellipse(surf, rim_color, (3, 19, 16, 5), 2)

    if frame % 2 == 0:
        pygame.draw.ellipse(surf, yellow, (2, 23, 9, 6))
        pygame.draw.ellipse(surf, yellow, (12, 24, 8, 5))
    else:
        pygame.draw.ellipse(surf, yellow, (4, 24, 8, 5))
        pygame.draw.ellipse(surf, yellow, (11, 23, 9, 6))

    return surf


def draw_mario_pixels(state: str = "idle", frame: int = 0) -> pygame.Surface:
    """Dibuja proceduralmente el sprite pixel art de Mario Pequeño (22x28)."""
    h = PLAYER_CROUCH_HEIGHT if state == "crouch" else PLAYER_HEIGHT
    surf = pygame.Surface((PLAYER_WIDTH, h), pygame.SRCALPHA)

    r = COLOR_MARIO_RED
    b = COLOR_MARIO_BROWN
    s = COLOR_MARIO_SKIN
    k = COLOR_BLACK

    if state == "crouch":
        pygame.draw.rect(surf, r, (4, 0, 14, 4))
        pygame.draw.rect(surf, r, (2, 2, 18, 3))
        pygame.draw.rect(surf, s, (4, 5, 12, 6))
        pygame.draw.rect(surf, k, (14, 6, 2, 3))
        pygame.draw.rect(surf, b, (12, 8, 6, 2))
        pygame.draw.rect(surf, b, (2, 11, 18, 5))
        pygame.draw.rect(surf, r, (6, 11, 8, 3))
        pygame.draw.rect(surf, b, (0, 15, 22, 3))
        return surf

    pygame.draw.rect(surf, r, (4, 0, 14, 4))
    pygame.draw.rect(surf, r, (2, 3, 18, 3))

    pygame.draw.rect(surf, s, (4, 6, 13, 7))
    pygame.draw.rect(surf, b, (2, 6, 4, 5))
    pygame.draw.rect(surf, k, (13, 7, 2, 3))
    pygame.draw.rect(surf, s, (15, 8, 4, 3))
    pygame.draw.rect(surf, b, (12, 10, 7, 3))

    pygame.draw.rect(surf, r, (3, 13, 16, 7))

    pygame.draw.rect(surf, b, (5, 14, 4, 6))
    pygame.draw.rect(surf, b, (11, 14, 4, 6))
    pygame.draw.rect(surf, b, (4, 18, 14, 4))

    if state == "jump":
        pygame.draw.rect(surf, b, (2, 20, 8, 4))
        pygame.draw.rect(surf, b, (12, 20, 8, 4))
        pygame.draw.rect(surf, b, (0, 24, 7, 4))
        pygame.draw.rect(surf, b, (14, 23, 8, 4))
    elif state == "walk":
        if frame % 2 == 0:
            pygame.draw.rect(surf, b, (3, 21, 6, 4))
            pygame.draw.rect(surf, b, (11, 21, 6, 4))
            pygame.draw.rect(surf, b, (0, 24, 8, 4))
            pygame.draw.rect(surf, b, (13, 24, 8, 4))
        else:
            pygame.draw.rect(surf, b, (5, 21, 5, 4))
            pygame.draw.rect(surf, b, (11, 21, 5, 4))
            pygame.draw.rect(surf, b, (3, 24, 7, 4))
            pygame.draw.rect(surf, b, (11, 24, 7, 4))
    else:
        pygame.draw.rect(surf, b, (4, 21, 5, 4))
        pygame.draw.rect(surf, b, (11, 21, 5, 4))
        pygame.draw.rect(surf, b, (2, 24, 7, 4))
        pygame.draw.rect(surf, b, (11, 24, 7, 4))

    return surf


def draw_super_mario_pixels(state: str = "idle", frame: int = 0) -> pygame.Surface:
    """Dibuja proceduralmente a Super Mario (24x48 px o agachado en 24x28 px)."""
    h = SUPER_MARIO_CROUCH_HEIGHT if state == "crouch" else SUPER_MARIO_HEIGHT
    surf = pygame.Surface((PLAYER_WIDTH + 2, h), pygame.SRCALPHA)

    r = COLOR_MARIO_RED
    b = COLOR_MARIO_BROWN
    s = COLOR_MARIO_SKIN
    k = COLOR_BLACK

    if state == "crouch":
        # Gorra
        pygame.draw.rect(surf, r, (4, 0, 16, 5))
        pygame.draw.rect(surf, r, (2, 3, 20, 4))
        # Cara
        pygame.draw.rect(surf, s, (4, 7, 14, 8))
        pygame.draw.rect(surf, k, (15, 8, 2, 4))
        pygame.draw.rect(surf, b, (13, 11, 7, 3))
        # Overol
        pygame.draw.rect(surf, b, (2, 15, 20, 8))
        pygame.draw.rect(surf, r, (6, 15, 10, 4))
        # Zapatos
        pygame.draw.rect(surf, b, (0, 23, 24, 5))
        return surf

    # 1. Gorra roja alta
    pygame.draw.rect(surf, r, (4, 0, 16, 6))
    pygame.draw.rect(surf, r, (2, 4, 20, 4))

    # 2. Cabeza y cara
    pygame.draw.rect(surf, s, (4, 8, 14, 10))
    pygame.draw.rect(surf, b, (2, 8, 4, 7))
    pygame.draw.rect(surf, k, (14, 10, 2, 4))
    pygame.draw.rect(surf, s, (16, 11, 5, 4))
    pygame.draw.rect(surf, b, (13, 14, 8, 4))

    # 3. Torso y Camisa
    pygame.draw.rect(surf, r, (2, 18, 20, 12))

    # 4. Overol Marrón / Azul
    pygame.draw.rect(surf, b, (4, 20, 5, 10))
    pygame.draw.rect(surf, b, (13, 20, 5, 10))
    pygame.draw.rect(surf, b, (3, 28, 18, 8))
    # Botones amarillos
    pygame.draw.rect(surf, (252, 216, 0), (6, 26, 2, 2))
    pygame.draw.rect(surf, (252, 216, 0), (14, 26, 2, 2))

    # 5. Piernas y Zapatos
    if state == "jump":
        pygame.draw.rect(surf, b, (1, 36, 10, 6))
        pygame.draw.rect(surf, b, (13, 36, 10, 6))
        pygame.draw.rect(surf, b, (0, 41, 9, 7))
        pygame.draw.rect(surf, b, (14, 40, 10, 7))
    elif state == "walk":
        if frame % 2 == 0:
            pygame.draw.rect(surf, b, (3, 36, 8, 6))
            pygame.draw.rect(surf, b, (13, 36, 8, 6))
            pygame.draw.rect(surf, b, (0, 42, 10, 6))
            pygame.draw.rect(surf, b, (14, 42, 10, 6))
        else:
            pygame.draw.rect(surf, b, (5, 36, 7, 6))
            pygame.draw.rect(surf, b, (12, 36, 7, 6))
            pygame.draw.rect(surf, b, (4, 42, 9, 6))
            pygame.draw.rect(surf, b, (12, 42, 9, 6))
    else:
        pygame.draw.rect(surf, b, (4, 36, 6, 6))
        pygame.draw.rect(surf, b, (12, 36, 6, 6))
        pygame.draw.rect(surf, b, (2, 42, 8, 6))
        pygame.draw.rect(surf, b, (12, 42, 8, 6))

    return surf

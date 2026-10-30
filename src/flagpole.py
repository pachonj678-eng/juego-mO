import pygame
from src.settings import TILE_SIZE, COLOR_BLACK, COLOR_WHITE
from src.audio import audio


def create_flag_surface() -> pygame.Surface:
    """Genera la bandera verde/blanca que ondea en el asta (24x18 px)."""
    surf = pygame.Surface((24, 18), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (0, 184, 0), [(0, 0), (22, 9), (0, 18)])
    pygame.draw.polygon(surf, COLOR_WHITE, [(2, 3), (16, 9), (2, 15)])
    pygame.draw.polygon(surf, (0, 184, 0), [(4, 6), (11, 9), (4, 12)])
    return surf


def create_castle_surface() -> pygame.Surface:
    """Genera la fachada del castillo de fin de fase estilo NES (128x128 px)."""
    surf = pygame.Surface((128, 128), pygame.SRCALPHA)
    brick_col = (196, 76, 16)
    highlight = (248, 136, 72)
    dark = COLOR_BLACK

    # 1. Cuerpo principal del castillo
    pygame.draw.rect(surf, brick_col, (16, 32, 96, 96))
    pygame.draw.rect(surf, dark, (16, 32, 96, 96), 2)

    # 2. Almenas / Torres superiores
    # Torre izquierda
    pygame.draw.rect(surf, brick_col, (16, 10, 24, 22))
    pygame.draw.rect(surf, dark, (16, 10, 24, 22), 2)
    # Almenas pequeñas torre izquierda
    for bx in (16, 32):
        pygame.draw.rect(surf, brick_col, (bx, 2, 8, 8))
        pygame.draw.rect(surf, dark, (bx, 2, 8, 8), 1)

    # Torre central
    pygame.draw.rect(surf, brick_col, (48, 16, 32, 16))
    pygame.draw.rect(surf, dark, (48, 16, 32, 16), 2)
    for bx in (48, 60, 72):
        pygame.draw.rect(surf, brick_col, (bx, 8, 8, 8))
        pygame.draw.rect(surf, dark, (bx, 8, 8, 8), 1)

    # Torre derecha
    pygame.draw.rect(surf, brick_col, (88, 10, 24, 22))
    pygame.draw.rect(surf, dark, (88, 10, 24, 22), 2)
    for bx in (88, 104):
        pygame.draw.rect(surf, brick_col, (bx, 2, 8, 8))
        pygame.draw.rect(surf, dark, (bx, 2, 8, 8), 1)

    # 3. Puerta de arco de entrada negra
    pygame.draw.rect(surf, dark, (48, 72, 32, 56), border_top_left_radius=16, border_top_right_radius=16)

    # Líneas de mortero decorativas
    for y in (48, 64, 80, 96, 112):
        pygame.draw.line(surf, dark, (18, y), (110, y), 1)

    return surf


class Flagpole:
    """
    Gestiona el asta de la bandera, la esfera dorada superior, la bandera deslizante,
    la detección de llegada y la cinemática de victoria hacia el castillo.
    """

    def __init__(self, x: int, base_y: int):
        self.x = float(x)
        self.base_y = float(base_y)
        self.height = 9 * TILE_SIZE  # 288 px de altura

        # Hitbox del mástil para colisión con Mario
        self.rect = pygame.Rect(round(self.x + 12), round(self.base_y - self.height), 8, self.height)

        # Bandera deslizante
        self.flag_surf = create_flag_surface()
        self.flag_x = self.x - 10
        self.flag_y = self.base_y - self.height + 14
        self.flag_target_y = self.base_y - 28

        # Estado de la cinemática
        self.is_triggered = False
        self.is_sliding = False
        self.is_walking_to_castle = False
        self.castle_x = self.x + 180.0
        self.castle_door_x = self.castle_x + 64.0
        self.castle_surf = create_castle_surface()

    def check_player(self, player) -> bool:
        """Comprueba si Mario toca el asta para iniciar la victoria."""
        if not self.is_triggered and self.rect.colliderect(player.rect):
            self.is_triggered = True
            self.is_sliding = True

            # Asignar puntaje según altura a la que Mario tocó el mástil
            touch_height = self.base_y - player.rect.centery
            if touch_height > 220:
                bonus = 5000
            elif touch_height > 150:
                bonus = 2000
            elif touch_height > 80:
                bonus = 800
            else:
                bonus = 400
            player.score += bonus

            # Ajustar posición de Mario fijado al mástil
            player.pos.x = float(self.x + 6)
            player.rect.x = round(player.pos.x)
            player.vel.x = 0.0
            player.vel.y = 150.0  # Velocidad de descenso controlado
            player.facing_right = True

            audio.play("flagpole")
            return True
        return False

    def update(self, dt: float, player) -> str:
        """
        Ejecuta la cinemática:
        1. Descenso de Mario y la bandera.
        2. Salto hacia el lado derecho del mástil.
        3. Caminata automática hacia la puerta del castillo.
        Devuelve el estado "PLAYING", "VICTORY_CINEMATIC" o "VICTORY_DONE".
        """
        if not self.is_triggered:
            return "PLAYING"

        # Fase 1: Descenso simultáneo por el mástil
        if self.is_sliding:
            # Descenso de la bandera
            if self.flag_y < self.flag_target_y:
                self.flag_y += 180.0 * dt
                if self.flag_y > self.flag_target_y:
                    self.flag_y = self.flag_target_y

            # Descenso de Mario
            player.pos.y += 150.0 * dt
            player.rect.y = round(player.pos.y)

            # Mario toca la base del mástil
            if player.rect.bottom >= self.base_y:
                player.rect.bottom = round(self.base_y)
                player.pos.y = float(player.rect.y)
                player.vel.y = 0.0

                # Pasar al lado derecho e iniciar marcha hacia el castillo
                self.is_sliding = False
                self.is_walking_to_castle = True
                player.pos.x = float(self.x + 24)
                player.rect.x = round(player.pos.x)
                player.vel.x = 110.0

            return "VICTORY_CINEMATIC"

        # Fase 2: Caminata automática hacia el interior del castillo
        if self.is_walking_to_castle:
            player.pos.x += 110.0 * dt
            player.rect.x = round(player.pos.x)
            player.current_state = "walk"
            player.anim_timer += dt * 8.0
            player.anim_frame = int(player.anim_timer) % 2
            player.update_animation(dt)

            # Mario entra al castillo y concluye la fase
            if player.pos.x >= self.castle_door_x:
                return "VICTORY_DONE"

            return "VICTORY_CINEMATIC"

        return "PLAYING"

    def draw(self, screen: pygame.Surface, camera):
        """Dibuja el mástil, la esfera dorada, la bandera y el castillo."""
        # 1. Dibujar el Castillo
        castle_screen_pos = camera.apply(pygame.Rect(round(self.castle_x), round(self.base_y - 96), 128, 128))
        screen.blit(self.castle_surf, castle_screen_pos)

        # 2. Bloque base de soporte del asta
        base_rect = camera.apply(pygame.Rect(round(self.x), round(self.base_y), TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, (216, 120, 48), base_rect)
        pygame.draw.rect(screen, COLOR_BLACK, base_rect, 1)

        # 3. Mástil metálico verde
        pole_screen_rect = camera.apply(self.rect)
        pygame.draw.rect(screen, (0, 168, 0), pole_screen_rect)
        pygame.draw.rect(screen, (120, 255, 120), (pole_screen_rect.x + 1, pole_screen_rect.y, 2, pole_screen_rect.height))
        pygame.draw.rect(screen, COLOR_BLACK, pole_screen_rect, 1)

        # 4. Esfera dorada superior
        top_center = (pole_screen_rect.centerx, pole_screen_rect.top - 4)
        pygame.draw.circle(screen, (252, 216, 0), top_center, 7)
        pygame.draw.circle(screen, COLOR_BLACK, top_center, 7, 1)

        # 5. Bandera deslizante
        flag_screen_rect = camera.apply(pygame.Rect(round(self.flag_x), round(self.flag_y), 24, 18))
        screen.blit(self.flag_surf, flag_screen_rect)

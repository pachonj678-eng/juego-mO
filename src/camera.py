import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    """
    Cámara 2D con desplazamiento horizontal suave y avance unidireccional estricto
    (estilo Super Mario Bros: la cámara no retrocede hacia la izquierda).
    """

    def __init__(self, level_width: int, level_height: int):
        self.level_width = level_width
        self.level_height = level_height
        self.offset_x = 0.0
        self.max_reached_x = 0.0  # Límite izquierdo estricto (nunca retrocede)

    def update(self, target_rect: pygame.Rect):
        """
        Centra la cámara en el objetivo si este avanza hacia la derecha,
        manteniendo fijo el avance sin retroceso.
        """
        # Queremos mantener al jugador aproximadamente a 1/3 del ancho de la pantalla
        desired_offset_x = target_rect.centerx - (SCREEN_WIDTH // 3)

        # Regla NES estricta: solo puede desplazarse hacia adelante
        if desired_offset_x > self.max_reached_x:
            self.max_reached_x = desired_offset_x

        # Limitar dentro de los bordes del nivel
        max_possible_x = max(0, self.level_width - SCREEN_WIDTH)
        self.offset_x = min(self.max_reached_x, max_possible_x)

    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        """Transforma un Rect del espacio del mundo al espacio de la pantalla."""
        return pygame.Rect(round(rect.x - self.offset_x), rect.y, rect.width, rect.height)

    def get_left_boundary(self) -> float:
        """Devuelve el límite izquierdo actual del mundo visible para el jugador."""
        return self.offset_x

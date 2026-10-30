import pygame
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH
from src.sprites import create_mushroom_surface, create_fireball_surface


class Mushroom(pygame.sprite.Sprite):
    """
    Ítem Champiñón que brota de un bloque [?], avanza horizontalmente por el suelo
    y transforma a Mario en Super Mario al ser recogido.
    """

    def __init__(self, x: float, y: float):
        super().__init__()
        self.image = create_mushroom_surface()
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(75.0, 0.0)  # Se desplaza a la derecha tras brotar
        self.gravity = 1200.0

        self.rect = self.image.get_rect(topleft=(round(x), round(y)))
        self.state = "emerging"
        self.target_y = y - 30.0  # Altura a la que debe ascender al brotar
        self.emerge_speed = -50.0

    def update(self, dt: float, solid_tiles: list):
        if self.state == "emerging":
            # Ascenso gradual desde el interior del bloque
            self.pos.y += self.emerge_speed * dt
            self.rect.y = round(self.pos.y)
            if self.pos.y <= self.target_y:
                self.pos.y = self.target_y
                self.rect.y = round(self.pos.y)
                self.state = "moving"
            return

        # Estado "moving": física con inercia, rebote en muros y caída
        # --- EJE X ---
        self.pos.x += self.vel.x * dt
        self.rect.x = round(self.pos.x)

        for tile in solid_tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.x > 0:
                    self.rect.right = tile.rect.left
                    self.vel.x = -abs(self.vel.x)
                elif self.vel.x < 0:
                    self.rect.left = tile.rect.right
                    self.vel.x = abs(self.vel.x)
                self.pos.x = float(self.rect.x)

        # --- EJE Y ---
        self.vel.y += self.gravity * dt
        self.pos.y += self.vel.y * dt
        self.rect.y = round(self.pos.y)

        for tile in solid_tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.vel.y = 0.0
                elif self.vel.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.vel.y = 0.0
                self.pos.y = float(self.rect.y)

        if self.rect.top > SCREEN_HEIGHT + 60:
            self.kill()


class Fireball(pygame.sprite.Sprite):
    """
    Proyectil Bola de Fuego arrojado por Mario.
    Rebota parabólicamente contra el suelo y fulmina enemigos al contacto.
    """

    def __init__(self, x: float, y: float, facing_right: bool):
        super().__init__()
        self.anim_timer = 0.0
        self.frame = 0
        self.image = create_fireball_surface(0)

        direction = 1 if facing_right else -1
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(360.0 * direction, 120.0)
        self.gravity = 1100.0
        self.bounce_impulse = -240.0

        self.rect = self.image.get_rect(center=(round(x), round(y)))

    def update(self, dt: float, solid_tiles: list):
        # 1. Animación giratoria
        self.anim_timer += dt
        if self.anim_timer >= 0.08:
            self.anim_timer = 0.0
            self.frame = (self.frame + 1) % 3
            self.image = create_fireball_surface(self.frame)

        # 2. Física Eje X
        self.pos.x += self.vel.x * dt
        self.rect.x = round(self.pos.x)

        for tile in solid_tiles:
            if self.rect.colliderect(tile.rect):
                # Al chocar contra una pared explota
                self.kill()
                return

        # 3. Física Eje Y
        self.vel.y += self.gravity * dt
        self.pos.y += self.vel.y * dt
        self.rect.y = round(self.pos.y)

        for tile in solid_tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.y > 0:
                    # Rebote contra el suelo
                    self.rect.bottom = tile.rect.top
                    self.vel.y = self.bounce_impulse
                    self.pos.y = float(self.rect.y)
                elif self.vel.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.vel.y = 0.0
                    self.pos.y = float(self.rect.y)

        if self.rect.top > SCREEN_HEIGHT + 30:
            self.kill()

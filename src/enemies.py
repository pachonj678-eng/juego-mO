import pygame
from src.settings import SCREEN_HEIGHT
from src.sprites import draw_goomba_pixels, draw_koopa_pixels
from src.audio import audio


class Enemy(pygame.sprite.Sprite):
    """
    Clase base para enemigos con IA de patrulla horizontal, gravedad y rebote en obstáculos.
    """

    def __init__(self, x: float, y: float, width: int, height: int, speed: float = 50.0):
        super().__init__()
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(-speed, 0.0)
        self.speed = speed
        self.gravity = 1200.0

        self.is_alive = True
        self.on_ground = False
        self.facing_right = False

        self.anim_timer = 0.0
        self.anim_frame = 0

        self.rect = pygame.Rect(round(x), round(y), width, height)

    def update_physics(self, dt: float, solid_tiles: list):
        self.pos.x += self.vel.x * dt
        self.rect.x = round(self.pos.x)

        for tile in solid_tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.x > 0:
                    self.rect.right = tile.rect.left
                    self.vel.x = -self.speed
                    self.facing_right = False
                elif self.vel.x < 0:
                    self.rect.left = tile.rect.right
                    self.vel.x = self.speed
                    self.facing_right = True
                self.pos.x = float(self.rect.x)

        self.vel.y += self.gravity * dt
        self.pos.y += self.vel.y * dt
        self.rect.y = round(self.pos.y)

        self.on_ground = False
        for tile in solid_tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.vel.y = 0.0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.vel.y = 0.0
                self.pos.y = float(self.rect.y)

        if self.rect.top > SCREEN_HEIGHT + 100:
            self.kill()


class Goomba(Enemy):
    """
    Enemigo Goomba clásico: patrulla constante, se aplasta al recibir un pisotón de Mario.
    """

    def __init__(self, x: float, y: float):
        super().__init__(x, y, width=24, height=24, speed=52.0)
        self.state = "walking"
        self.flatten_timer = 0.0
        self.image = draw_goomba_pixels("walk", 0)

    def update(self, dt: float, solid_tiles: list):
        if self.state == "flattened":
            self.flatten_timer += dt
            if self.flatten_timer >= 0.45:
                self.kill()
            return

        self.update_physics(dt, solid_tiles)

        self.anim_timer += dt * 6.0
        self.anim_frame = int(self.anim_timer) % 2
        self.image = draw_goomba_pixels("walk", self.anim_frame)

    def on_stomp(self, player) -> bool:
        if self.state == "walking":
            self.state = "flattened"
            self.vel.x = 0.0
            self.vel.y = 0.0
            self.image = draw_goomba_pixels("flattened")
            old_bottom = self.rect.bottom
            self.rect.height = 10
            self.rect.bottom = old_bottom
            self.pos.y = float(self.rect.y)

            player.score += 100
            audio.play("stomp")
            return True
        return False

    def on_player_collision(self, player):
        if self.state == "walking":
            player.take_damage()


class Koopa(Enemy):
    """
    Enemigo Koopa Troopa:
    1. Caminando ("walking"): al recibir pisotón se retrae en caparazón ("shell_idle").
    2. Caparazón quieto ("shell_idle"): Mario lo patea para dispararlo a alta velocidad ("shell_sliding").
    3. Caparazón deslizante ("shell_sliding"): elimina enemigos al chocar y rebota en paredes.
    """

    def __init__(self, x: float, y: float):
        super().__init__(x, y, width=24, height=30, speed=58.0)
        self.state = "walking"
        self.slide_speed = 380.0
        self.image = draw_koopa_pixels("walk", 0)

    def update(self, dt: float, solid_tiles: list):
        if self.state == "shell_idle":
            self.vel.x = 0.0
            self.update_physics(dt, solid_tiles)
            self.image = draw_koopa_pixels("shell", 0)
            return

        if self.state == "shell_sliding":
            self.speed = self.slide_speed
            self.update_physics(dt, solid_tiles)
            self.image = draw_koopa_pixels("shell", 0)
            return

        self.speed = 58.0
        self.update_physics(dt, solid_tiles)

        self.anim_timer += dt * 6.0
        self.anim_frame = int(self.anim_timer) % 2
        base_surf = draw_koopa_pixels("walk", self.anim_frame)

        if self.vel.x > 0:
            self.image = pygame.transform.flip(base_surf, True, False)
        else:
            self.image = base_surf

    def kick(self, player):
        direction = 1 if player.rect.centerx < self.rect.centerx else -1
        self.state = "shell_sliding"
        self.vel.x = direction * self.slide_speed
        player.score += 200
        audio.play("stomp")

    def on_stomp(self, player) -> bool:
        if self.state == "walking":
            self.state = "shell_idle"
            self.vel.x = 0.0
            old_bottom = self.rect.bottom
            self.rect.height = 20
            self.rect.bottom = old_bottom
            self.pos.y = float(self.rect.y)
            self.image = draw_koopa_pixels("shell", 0)
            player.score += 100
            audio.play("stomp")
            return True

        elif self.state == "shell_sliding":
            self.state = "shell_idle"
            self.vel.x = 0.0
            player.score += 100
            audio.play("stomp")
            return True

        elif self.state == "shell_idle":
            self.kick(player)
            return True

        return False

    def on_player_collision(self, player):
        if self.state == "walking":
            player.take_damage()
        elif self.state == "shell_idle":
            self.kick(player)
        elif self.state == "shell_sliding":
            player.take_damage()

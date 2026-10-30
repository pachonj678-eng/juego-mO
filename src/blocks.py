import pygame
from src.settings import TILE_SIZE, SCREEN_HEIGHT
from src.sprites import (
    create_question_block,
    create_empty_block,
    create_brick_block,
    create_coin_surface,
    create_brick_debris_surface
)
from src.audio import audio


class BouncingCoin(pygame.sprite.Sprite):
    """
    Moneda que brota del bloque [?] al ser golpeado desde abajo.
    Asciende girando y cae brevemente antes de desaparecer sumando puntos.
    """

    def __init__(self, x: float, y: float):
        super().__init__()
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.vel_y = -380.0
        self.gravity = 1300.0
        self.initial_y = float(y)

        self.anim_timer = 0.0
        self.frame = 0
        self.image = create_coin_surface(0)
        self.rect = self.image.get_rect(topleft=(round(self.pos_x), round(self.pos_y)))
        audio.play("coin")

    def update(self, dt: float):
        self.vel_y += self.gravity * dt
        self.pos_y += self.vel_y * dt
        self.rect.y = round(self.pos_y)

        self.anim_timer += dt
        if self.anim_timer >= 0.06:
            self.anim_timer = 0.0
            self.frame = (self.frame + 1) % 4
            self.image = create_coin_surface(self.frame)

        if self.vel_y > 0 and self.pos_y >= self.initial_y - 8:
            self.kill()


class FloatingCoin(pygame.sprite.Sprite):
    """
    Moneda flotante coleccionable situada en el mundo que Mario recoge al pasar.
    """

    def __init__(self, x: int, y: int):
        super().__init__()
        self.anim_timer = 0.0
        self.frame = 0
        self.image = create_coin_surface(0)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt: float):
        self.anim_timer += dt
        if self.anim_timer >= 0.12:
            self.anim_timer = 0.0
            self.frame = (self.frame + 1) % 4
            self.image = create_coin_surface(self.frame)

    def collect(self, player) -> int:
        player.coins += 1
        player.score += 200
        audio.play("coin")
        self.kill()
        return 200


class BrickDebris(pygame.sprite.Sprite):
    """
    Partícula/fragmento de ladrillo expulsado al romper un bloque de ladrillos.
    """

    def __init__(self, x: float, y: float, vel_x: float, vel_y: float):
        super().__init__()
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(vel_x, vel_y)
        self.gravity = 1200.0
        self.image = create_brick_debris_surface()
        self.rect = self.image.get_rect(center=(round(x), round(y)))

    def update(self, dt: float):
        self.vel.y += self.gravity * dt
        self.pos += self.vel * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if self.rect.top > SCREEN_HEIGHT + 50:
            self.kill()


class InteractiveBlock(pygame.sprite.Sprite):
    """
    Clase base para bloques que rebotan hacia arriba al ser golpeados desde abajo.
    """

    def __init__(self, x: int, y: int, surface: pygame.Surface, block_type: str):
        super().__init__()
        self.image = surface
        self.base_x = float(x)
        self.base_y = float(y)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.block_type = block_type

        self.is_bumping = False
        self.bump_timer = 0.0
        self.bump_duration = 0.16
        self.bump_max_height = 8.0

    def trigger_bump(self):
        if not self.is_bumping:
            self.is_bumping = True
            self.bump_timer = 0.0

    def update_bump(self, dt: float):
        if self.is_bumping:
            self.bump_timer += dt
            half = self.bump_duration / 2.0

            if self.bump_timer <= half:
                progress = self.bump_timer / half
                offset_y = -self.bump_max_height * progress
            elif self.bump_timer <= self.bump_duration:
                progress = (self.bump_timer - half) / half
                offset_y = -self.bump_max_height * (1.0 - progress)
            else:
                offset_y = 0.0
                self.is_bumping = False

            self.rect.y = round(self.base_y + offset_y)
        else:
            self.rect.y = round(self.base_y)


class QuestionBlock(InteractiveBlock):
    """
    Bloque misterioso [?] que al golpearlo desde abajo suelta moneda o champiñón
    y se transforma en bloque usado/inactivo.
    """

    def __init__(self, x: int, y: int, content: str = "coin"):
        super().__init__(x, y, create_question_block(0), "question")
        self.content = content
        self.is_empty = False

        self.anim_timer = 0.0
        self.anim_frame = 0

    def update(self, dt: float):
        self.update_bump(dt)

        if not self.is_empty:
            self.anim_timer += dt
            if self.anim_timer >= 0.18:
                self.anim_timer = 0.0
                self.anim_frame = (self.anim_frame + 1) % 4
                self.image = create_question_block(self.anim_frame)

    def hit_from_below(self, player) -> list:
        if self.is_empty:
            self.trigger_bump()
            return []

        self.is_empty = True
        self.image = create_empty_block()
        self.trigger_bump()

        spawned = []
        if self.content == "coin":
            player.coins += 1
            player.score += 200
            coin = BouncingCoin(self.base_x, self.base_y - TILE_SIZE)
            spawned.append(coin)
        elif self.content == "mushroom":
            from src.items import Mushroom
            mushroom = Mushroom(self.base_x + 4, self.base_y)
            spawned.append(mushroom)

        return spawned


class BrickBlock(InteractiveBlock):
    """
    Bloque de ladrillo destructible.
    Rebota si Mario es pequeño; se destruye en 4 partes si Mario está en modo Super.
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y, create_brick_block(), "brick")

    def update(self, dt: float):
        self.update_bump(dt)

    def hit_from_below(self, player) -> list:
        spawned = []

        if getattr(player, "is_big", False):
            cx = self.rect.centerx
            cy = self.rect.centery
            player.score += 50
            audio.play("brick")

            spawned.append(BrickDebris(cx - 6, cy - 6, vel_x=-120.0, vel_y=-420.0))
            spawned.append(BrickDebris(cx + 6, cy - 6, vel_x=120.0, vel_y=-420.0))
            spawned.append(BrickDebris(cx - 6, cy + 6, vel_x=-80.0, vel_y=-260.0))
            spawned.append(BrickDebris(cx + 6, cy + 6, vel_x=80.0, vel_y=-260.0))

            self.kill()
        else:
            self.trigger_bump()

        return spawned

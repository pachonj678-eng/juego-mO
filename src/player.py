import pygame
from src.settings import (
    WALK_ACCELERATION,
    RUN_ACCELERATION,
    GROUND_FRICTION,
    SKID_FRICTION,
    AIR_FRICTION,
    MAX_WALK_SPEED,
    MAX_RUN_SPEED,
    GRAVITY,
    JUMP_INITIAL_VELOCITY,
    JUMP_HOLD_FORCE,
    MAX_JUMP_HOLD_TIME,
    FALL_GRAVITY_MULTIPLIER,
    TERMINAL_VELOCITY,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_CROUCH_HEIGHT,
    SCREEN_HEIGHT,
    TILE_SIZE,
    KEYS_MOVE_LEFT,
    KEYS_MOVE_RIGHT,
    KEYS_JUMP,
    KEYS_RUN,
    KEYS_CROUCH
)
from src.sprites import (
    draw_mario_pixels,
    draw_super_mario_pixels,
    SUPER_MARIO_HEIGHT,
    SUPER_MARIO_CROUCH_HEIGHT
)
from src.items import Fireball
from src.audio import audio


class Player(pygame.sprite.Sprite):
    """
    Controlador de jugador (Mario) con soporte completo para:
    - Estado Pequeño vs. Super Mario (con transformación de altura y animación de crecimiento).
    - Disparo de proyectiles de bola de fuego con Shift.
    - Físicas con inercia, derrape, salto variable y agachado.
    - Invulnerabilidad con parpadeo tras recibir daño.
    - Efectos de audio retro sintetizados.
    """

    def __init__(self, x: float, y: float):
        super().__init__()

        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0.0, 0.0)
        self.facing_right = True

        self.score = 0
        self.coins = 0
        self.lives = 3
        self.is_big = False

        self.growth_timer = 0.0
        self.shoot_cooldown = 0.0

        self.invincible = False
        self.invincible_timer = 0.0
        self.is_flashing = False

        self.on_ground = False
        self.is_jumping = False
        self.jump_hold_timer = 0.0
        self.is_crouching = False
        self.is_running = False

        self.rect = pygame.Rect(round(x), round(y), PLAYER_WIDTH, PLAYER_HEIGHT)

        self.anim_timer = 0.0
        self.anim_frame = 0
        self.current_state = "idle"
        self.image = draw_mario_pixels("idle", 0)

    def power_up(self, item_type: str = "mushroom"):
        """Transforma a Mario en Super Mario al recoger un Champiñón."""
        if not self.is_big:
            self.is_big = True
            self.score += 1000

            old_bottom = self.rect.bottom
            self.rect.height = SUPER_MARIO_HEIGHT
            self.rect.bottom = old_bottom
            self.pos.y = float(self.rect.y)

            self.growth_timer = 0.6
            self.invincible = True
            self.invincible_timer = max(self.invincible_timer, 0.8)
            audio.play("powerup")

    def take_damage(self):
        """Gestiona el daño recibido."""
        if self.invincible or self.growth_timer > 0:
            return

        if self.is_big:
            self.is_big = False
            old_bottom = self.rect.bottom
            self.rect.height = PLAYER_HEIGHT
            self.rect.bottom = old_bottom
            self.pos.y = float(self.rect.y)

            self.invincible = True
            self.invincible_timer = 2.5
            self.vel.y = -220.0
        else:
            self.lives -= 1
            self.invincible = True
            self.invincible_timer = 2.5
            self.pos = pygame.Vector2(64, SCREEN_HEIGHT - (4 * TILE_SIZE))
            self.vel = pygame.Vector2(0.0, 0.0)
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

    def handle_input(self, keys: pygame.key.ScancodeWrapper, dt: float) -> list:
        """Procesa controles y disparo de proyectiles."""
        spawned_projectiles = []

        move_left = any(keys[k] for k in KEYS_MOVE_LEFT)
        move_right = any(keys[k] for k in KEYS_MOVE_RIGHT)
        jump_pressed = any(keys[k] for k in KEYS_JUMP)
        crouch_pressed = any(keys[k] for k in KEYS_CROUCH)
        self.is_running = any(keys[k] for k in KEYS_RUN)

        if crouch_pressed and self.on_ground:
            self.is_crouching = True
        else:
            self.is_crouching = False

        if self.is_big:
            target_height = SUPER_MARIO_CROUCH_HEIGHT if self.is_crouching else SUPER_MARIO_HEIGHT
        else:
            target_height = PLAYER_CROUCH_HEIGHT if self.is_crouching else PLAYER_HEIGHT

        if self.rect.height != target_height:
            diff = self.rect.height - target_height
            self.rect.height = target_height
            self.pos.y += diff
            self.rect.y = round(self.pos.y)

        input_dir = 0
        if not (self.is_crouching and self.on_ground):
            if move_left and not move_right:
                input_dir = -1
                self.facing_right = False
            elif move_right and not move_left:
                input_dir = 1
                self.facing_right = True

        accel_rate = RUN_ACCELERATION if self.is_running else WALK_ACCELERATION
        max_speed = MAX_RUN_SPEED if self.is_running else MAX_WALK_SPEED

        if input_dir != 0:
            if (input_dir > 0 and self.vel.x < 0) or (input_dir < 0 and self.vel.x > 0):
                self.vel.x += input_dir * SKID_FRICTION * dt
            else:
                self.vel.x += input_dir * accel_rate * dt

            if abs(self.vel.x) > max_speed:
                self.vel.x = max_speed if self.vel.x > 0 else -max_speed
        else:
            friction = GROUND_FRICTION if self.on_ground else AIR_FRICTION
            if self.vel.x > 0:
                self.vel.x = max(0.0, self.vel.x - friction * dt)
            elif self.vel.x < 0:
                self.vel.x = min(0.0, self.vel.x + friction * dt)

        # Salto Variable
        if jump_pressed:
            if self.on_ground and not self.is_jumping:
                self.vel.y = JUMP_INITIAL_VELOCITY
                self.on_ground = False
                self.is_jumping = True
                self.jump_hold_timer = 0.0
                audio.play("jump")
            elif self.is_jumping and self.jump_hold_timer < MAX_JUMP_HOLD_TIME:
                self.jump_hold_timer += dt
                self.vel.y += JUMP_HOLD_FORCE * dt
        else:
            if self.is_jumping:
                self.is_jumping = False
                if self.vel.y < -120.0:
                    self.vel.y = -120.0

        # Disparo con Shift
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        if self.is_running and self.shoot_cooldown <= 0:
            if self.is_big:
                spawn_x = self.rect.right if self.facing_right else self.rect.left
                spawn_y = self.rect.centery - 4
                ball = Fireball(spawn_x, spawn_y, self.facing_right)
                spawned_projectiles.append(ball)
                self.shoot_cooldown = 0.32
                audio.play("fireball")

        return spawned_projectiles

    def apply_gravity(self, dt: float):
        multiplier = FALL_GRAVITY_MULTIPLIER if self.vel.y > 0 else 1.0
        self.vel.y += GRAVITY * multiplier * dt
        if self.vel.y > TERMINAL_VELOCITY:
            self.vel.y = TERMINAL_VELOCITY

    def update_physics(self, dt: float, solid_tiles: list, camera_left: float) -> list:
        spawned_entities = []

        # EJE X
        self.pos.x += self.vel.x * dt
        self.rect.x = round(self.pos.x)

        if self.rect.left < camera_left:
            self.rect.left = round(camera_left)
            self.pos.x = float(self.rect.x)
            if self.vel.x < 0:
                self.vel.x = 0.0

        for tile in solid_tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.x > 0:
                    self.rect.right = tile.rect.left
                    self.vel.x = 0.0
                elif self.vel.x < 0:
                    self.rect.left = tile.rect.right
                    self.vel.x = 0.0
                self.pos.x = float(self.rect.x)

        # EJE Y
        self.pos.y += self.vel.y * dt
        self.rect.y = round(self.pos.y)

        self.on_ground = False

        for tile in list(solid_tiles):
            if self.rect.colliderect(tile.rect):
                if self.vel.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.vel.y = 0.0
                    self.on_ground = True
                    self.is_jumping = False
                elif self.vel.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.vel.y = 0.0

                    if hasattr(tile, "hit_from_below"):
                        new_items = tile.hit_from_below(self)
                        if new_items:
                            spawned_entities.extend(new_items)
                        if not tile.alive() and tile in solid_tiles:
                            solid_tiles.remove(tile)

                self.pos.y = float(self.rect.y)

        return spawned_entities

    def update_animation(self, dt: float):
        if not self.on_ground:
            self.current_state = "jump"
        elif self.is_crouching:
            self.current_state = "crouch"
        elif abs(self.vel.x) > 10.0:
            self.current_state = "walk"
            self.anim_timer += dt * (abs(self.vel.x) / 18.0)
            self.anim_frame = int(self.anim_timer) % 2
        else:
            self.current_state = "idle"
            self.anim_frame = 0

        show_as_super = self.is_big
        if self.growth_timer > 0:
            self.growth_timer -= dt
            show_as_super = (int(self.growth_timer * 16) % 2 == 0)

        if show_as_super:
            base_surf = draw_super_mario_pixels(self.current_state, self.anim_frame)
        else:
            base_surf = draw_mario_pixels(self.current_state, self.anim_frame)

        if not self.facing_right:
            base_surf = pygame.transform.flip(base_surf, True, False)

        if self.invincible and self.growth_timer <= 0:
            if int(self.invincible_timer * 12) % 2 == 0:
                ghost_surf = base_surf.copy()
                ghost_surf.set_alpha(90)
                self.image = ghost_surf
            else:
                self.image = base_surf
        else:
            self.image = base_surf

    def update(self, dt: float, keys: pygame.key.ScancodeWrapper, solid_tiles: list, camera_left: float) -> list:
        if self.invincible and self.growth_timer <= 0:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0.0:
                self.invincible = False
                self.invincible_timer = 0.0

        projectiles = self.handle_input(keys, dt)
        self.apply_gravity(dt)
        spawned = self.update_physics(dt, solid_tiles, camera_left)
        self.update_animation(dt)

        return spawned + projectiles

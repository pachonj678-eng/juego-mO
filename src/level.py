import pygame
from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    TILE_SIZE,
    COLOR_SKY,
    KEYS_JUMP
)
from src.sprites import (
    create_ground_tile,
    create_solid_block,
    create_pipe_tile
)
from src.blocks import (
    QuestionBlock,
    BrickBlock,
    FloatingCoin,
    BouncingCoin,
    BrickDebris
)
from src.items import Mushroom, Fireball
from src.enemies import Goomba, Koopa
from src.player import Player
from src.camera import Camera
from src.flagpole import Flagpole


class Tile(pygame.sprite.Sprite):
    """Representa un bloque o terreno sólido estándar en el nivel."""

    def __init__(self, x: int, y: int, surface: pygame.Surface, tile_type: str = "ground"):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(topleft=(x, y))
        self.tile_type = tile_type


class Level:
    """
    Gestiona el nivel completo, temporizador de 400s, estados de juego
    (PLAYING, VICTORY, GAME_OVER), asta de bandera, castillo y cámara.
    """

    def __init__(self):
        self.reset_level()

    def reset_level(self):
        """Reinicia el nivel a su estado inicial para una nueva partida o reinicio."""
        self.tiles = pygame.sprite.Group()
        self.interactive_blocks = pygame.sprite.Group()
        self.floating_coins = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.solid_tiles = []

        # Longitud completa del nivel: 90 tiles (2880 px)
        self.level_width = 90 * TILE_SIZE
        self.level_height = SCREEN_HEIGHT

        self.camera = Camera(self.level_width, self.level_height)
        self.player = Player(x=64, y=SCREEN_HEIGHT - (4 * TILE_SIZE))

        # Asta de bandera en columna 74
        self.flagpole = Flagpole(x=74 * TILE_SIZE, base_y=12 * TILE_SIZE)

        # Temporizador clásico de 400 segundos (disminuye 2.5 unidades por segundo real)
        self.time_left = 400.0
        self.game_state = "PLAYING"  # "PLAYING", "VICTORY", "GAME_OVER"
        self.time_bonus_calculated = False

        self._build_level()

    def _build_level(self):
        """Construye el recorrido íntegro inspirado en Super Mario Bros World 1-1."""
        ground_img = create_ground_tile()
        solid_img = create_solid_block()
        pipe_tl = create_pipe_tile(is_top=True, is_left=True)
        pipe_tr = create_pipe_tile(is_top=True, is_left=False)
        pipe_bl = create_pipe_tile(is_top=False, is_left=True)
        pipe_br = create_pipe_tile(is_top=False, is_left=False)

        # 1. Suelo continuo con fosos
        for col in range(90):
            if col in (24, 25, 52, 53):
                continue
            for row in (13, 14):
                tile = Tile(col * TILE_SIZE, row * TILE_SIZE, ground_img, "ground")
                self.tiles.add(tile)
                self.solid_tiles.append(tile)

        # 2. Tubería 1 (columna 12 y 13)
        p1 = [
            Tile(12 * TILE_SIZE, 11 * TILE_SIZE, pipe_tl, "pipe"),
            Tile(13 * TILE_SIZE, 11 * TILE_SIZE, pipe_tr, "pipe"),
            Tile(12 * TILE_SIZE, 12 * TILE_SIZE, pipe_bl, "pipe"),
            Tile(13 * TILE_SIZE, 12 * TILE_SIZE, pipe_br, "pipe")
        ]
        for p in p1:
            self.tiles.add(p)
            self.solid_tiles.append(p)

        # 3. Bloque [?] solitario (columna 9)
        q1 = QuestionBlock(9 * TILE_SIZE, 9 * TILE_SIZE, content="coin")
        self.interactive_blocks.add(q1)
        self.solid_tiles.append(q1)

        # 4. Formación World 1-1: [Ladrillo] [?] [Ladrillo] [?] [Ladrillo] (columnas 17 a 21)
        pattern = [
            (17, "brick", None),
            (18, "question", "mushroom"),
            (19, "brick", None),
            (20, "question", "coin"),
            (21, "brick", None)
        ]
        for col_idx, b_type, content in pattern:
            if b_type == "question":
                b = QuestionBlock(col_idx * TILE_SIZE, 9 * TILE_SIZE, content=content)
            else:
                b = BrickBlock(col_idx * TILE_SIZE, 9 * TILE_SIZE)
            self.interactive_blocks.add(b)
            self.solid_tiles.append(b)

        # Bloque elevado
        q_high = QuestionBlock(19 * TILE_SIZE, 5 * TILE_SIZE, content="coin")
        self.interactive_blocks.add(q_high)
        self.solid_tiles.append(q_high)

        # 5. Monedas flotantes sobre foso
        self.floating_coins.add(FloatingCoin(23 * TILE_SIZE, 10 * TILE_SIZE))
        self.floating_coins.add(FloatingCoin(24 * TILE_SIZE, 8 * TILE_SIZE))
        self.floating_coins.add(FloatingCoin(25 * TILE_SIZE, 10 * TILE_SIZE))

        # Plataforma de ladrillos intermedia con monedas
        for c in range(31, 35):
            self.floating_coins.add(FloatingCoin(c * TILE_SIZE, 6 * TILE_SIZE))
            brick = BrickBlock(c * TILE_SIZE, 7 * TILE_SIZE)
            self.interactive_blocks.add(brick)
            self.solid_tiles.append(brick)

        # 6. Pirámide intermedia (columnas 40 a 44)
        for step in range(4):
            col_start = 40 + step
            for col in range(col_start, 44):
                row = 12 - step
                blk = Tile(col * TILE_SIZE, row * TILE_SIZE, solid_img, "solid")
                self.tiles.add(blk)
                self.solid_tiles.append(blk)

        # 7. Escalera Final monumental hacia el Asta de Bandera (columnas 64 a 71)
        # 8 peldaños ascendentes que culminan en la cima
        for step in range(8):
            col_start = 64 + step
            for col in range(col_start, 72):
                row = 12 - step
                blk = Tile(col * TILE_SIZE, row * TILE_SIZE, solid_img, "solid")
                self.tiles.add(blk)
                self.solid_tiles.append(blk)

        # 8. Enemigos distribuidos
        self.enemies.add(Goomba(15 * TILE_SIZE, 12 * TILE_SIZE))
        self.enemies.add(Goomba(27 * TILE_SIZE, 12 * TILE_SIZE))
        self.enemies.add(Goomba(29 * TILE_SIZE, 12 * TILE_SIZE))
        self.enemies.add(Koopa(36 * TILE_SIZE, 11 * TILE_SIZE))
        self.enemies.add(Koopa(46 * TILE_SIZE, 11 * TILE_SIZE))
        self.enemies.add(Goomba(58 * TILE_SIZE, 12 * TILE_SIZE))

    def update(self, dt: float, keys: pygame.key.ScancodeWrapper):
        """Ciclo de actualización principal."""
        if self.game_state == "GAME_OVER" or self.game_state == "VICTORY":
            return

        # 1. Temporizador del nivel (cuenta atrás)
        if not self.flagpole.is_triggered:
            self.time_left -= dt * 2.5
            if self.time_left <= 0.0:
                self.time_left = 0.0
                self.player.lives = 0
                self.game_state = "GAME_OVER"
                return

        # 2. Comprobar Fin de Vidas
        if self.player.lives <= 0:
            self.game_state = "GAME_OVER"
            return

        # 3. Actualizar bloques, monedas y partículas
        self.interactive_blocks.update(dt)
        self.floating_coins.update(dt)
        self.particles.update(dt)

        for item in self.items:
            item.update(dt, self.solid_tiles)

        for ball in self.fireballs:
            ball.update(dt, self.solid_tiles)

        # 4. Cinemática de Bandera / Asta de Victoria
        self.flagpole.check_player(self.player)
        flag_status = self.flagpole.update(dt, self.player)

        if flag_status == "VICTORY_DONE":
            self.game_state = "VICTORY"
            if not self.time_bonus_calculated:
                self.time_bonus_calculated = True
                self.player.score += int(self.time_left) * 50
            return

        # Si está en plena cinemática de victoria, la cámara sigue a Mario y no procesa enemigos
        if flag_status == "VICTORY_CINEMATIC":
            self.camera.update(self.player.rect)
            return

        # 5. Modo Normal de Juego
        for enemy in self.enemies:
            enemy.update(dt, self.solid_tiles)

        spawned = self.player.update(dt, keys, self.solid_tiles, self.camera.get_left_boundary())
        for entity in spawned:
            if isinstance(entity, Mushroom):
                self.items.add(entity)
            elif isinstance(entity, Fireball):
                self.fireballs.add(entity)
            else:
                self.particles.add(entity)

        # Colisión con Champiñones
        for item in pygame.sprite.spritecollide(self.player, self.items, False):
            if isinstance(item, Mushroom) and item.state == "moving":
                self.player.power_up("mushroom")
                item.kill()

        # Bolas de Fuego contra Enemigos
        for ball in self.fireballs:
            for enemy in pygame.sprite.spritecollide(ball, self.enemies, False):
                if enemy.alive():
                    enemy.kill()
                    self.player.score += 200
                    ball.kill()
                    break

        # Mario contra Enemigos (Stomp o Daño)
        jump_held = any(keys[k] for k in KEYS_JUMP)
        for enemy in list(self.enemies):
            if not enemy.alive():
                continue
            if isinstance(enemy, Goomba) and enemy.state == "flattened":
                continue

            if self.player.rect.colliderect(enemy.rect):
                is_falling_on_top = (self.player.vel.y > 0) and (self.player.rect.bottom <= enemy.rect.centery + 12)

                if is_falling_on_top:
                    stomp_success = enemy.on_stomp(self.player)
                    if stomp_success:
                        bounce_force = -420.0 if jump_held else -310.0
                        self.player.vel.y = bounce_force
                        self.player.on_ground = False
                else:
                    enemy.on_player_collision(self.player)

        # Caparazón Koopa en deslizamiento
        for enemy in self.enemies:
            if isinstance(enemy, Koopa) and enemy.state == "shell_sliding":
                for target in list(self.enemies):
                    if target != enemy and target.alive():
                        if enemy.rect.colliderect(target.rect):
                            target.kill()
                            self.player.score += 200

        # Monedas flotantes
        for coin in pygame.sprite.spritecollide(self.player, self.floating_coins, False):
            coin.collect(self.player)

        # Caída por fosos
        if self.player.pos.y > SCREEN_HEIGHT + 50:
            self.player.take_damage()

        # Actualizar cámara
        self.camera.update(self.player.rect)

    def draw_scenery(self, screen: pygame.Surface):
        screen.fill(COLOR_SKY)
        cloud_color = (240, 248, 255)
        for base_x in (100, 350, 700, 1100, 1500, 2000, 2400, 2800):
            screen_x = base_x - (self.camera.offset_x * 0.4)
            if -100 <= screen_x <= SCREEN_WIDTH + 100:
                pygame.draw.circle(screen, cloud_color, (round(screen_x), 80), 24)
                pygame.draw.circle(screen, cloud_color, (round(screen_x + 20), 75), 30)
                pygame.draw.circle(screen, cloud_color, (round(screen_x + 40), 80), 22)

    def draw(self, screen: pygame.Surface):
        self.draw_scenery(screen)
        cam_rect = pygame.Rect(self.camera.offset_x - 32, 0, SCREEN_WIDTH + 64, SCREEN_HEIGHT)

        # 1. Terreno y tuberías
        for tile in self.tiles:
            if cam_rect.colliderect(tile.rect):
                screen.blit(tile.image, self.camera.apply(tile.rect))

        # 2. Bloques interactivos
        for block in self.interactive_blocks:
            if cam_rect.colliderect(block.rect):
                screen.blit(block.image, self.camera.apply(block.rect))

        # 3. Monedas flotantes
        for coin in self.floating_coins:
            if cam_rect.colliderect(coin.rect):
                screen.blit(coin.image, self.camera.apply(coin.rect))

        # 4. Ítems (Champiñones)
        for item in self.items:
            if cam_rect.colliderect(item.rect):
                screen.blit(item.image, self.camera.apply(item.rect))

        # 5. Asta de Bandera y Castillo
        self.flagpole.draw(screen, self.camera)

        # 6. Proyectiles
        for ball in self.fireballs:
            screen.blit(ball.image, self.camera.apply(ball.rect))

        # 7. Enemigos
        for enemy in self.enemies:
            if cam_rect.colliderect(enemy.rect):
                screen.blit(enemy.image, self.camera.apply(enemy.rect))

        # 8. Partículas
        for particle in self.particles:
            screen.blit(particle.image, self.camera.apply(particle.rect))

        # 9. Mario (si no ha entrado ya a la puerta final del castillo)
        if self.game_state != "VICTORY":
            screen.blit(self.player.image, self.camera.apply(self.player.rect))

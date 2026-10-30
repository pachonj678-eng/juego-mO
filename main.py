import sys
import pygame
from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    KEYS_PAUSE,
    COLOR_WHITE,
    COLOR_BLACK
)
from src.level import Level


def main():
    """Punto de entrada principal con HUD completo, cinemáticas y pantallas de fin de juego."""
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Super Mario Bros 2D - Producción Final")
    clock = pygame.time.Clock()

    hud_font = pygame.font.SysFont("Courier New", 18, bold=True)
    title_font = pygame.font.SysFont("Arial", 32, bold=True)
    sub_font = pygame.font.SysFont("Arial", 16, bold=True)
    guide_font = pygame.font.SysFont("Arial", 13, bold=True)

    level = Level()
    is_paused = False
    running = True

    while running:
        raw_dt = clock.tick(FPS) / 1000.0
        dt = min(raw_dt, 0.05)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in KEYS_PAUSE:
                    if level.game_state == "PLAYING":
                        is_paused = not is_paused

                # Reinicio de partida con R o Enter al terminar
                elif event.key in (pygame.K_r, pygame.K_RETURN):
                    if level.game_state in ("VICTORY", "GAME_OVER"):
                        level.reset_level()

                # Toggle Super Mario para pruebas con B
                elif event.key == pygame.K_b and level.game_state == "PLAYING":
                    if not level.player.is_big:
                        level.player.power_up("mushroom")
                    else:
                        level.player.take_damage()

        # Actualización de Lógica
        if not is_paused:
            keys = pygame.key.get_pressed()
            level.update(dt, keys)

        # Renderizado del Mundo
        level.draw(screen)

        # HUD Superior Clásico de Super Mario Bros
        player = level.player
        time_int = max(0, int(level.time_left))

        score_str = f"MARIO\n{player.score:06d}"
        coins_str = f"COINS\n*{player.coins:02d}"
        world_str = "WORLD\n 1-1"
        time_str = f"TIME\n {time_int:03d}"
        lives_str = f"LIVES\n x{player.lives}"

        hud_items = [
            (score_str, 25),
            (coins_str, 185),
            (world_str, 345),
            (time_str, 505),
            (lives_str, 665)
        ]

        for text, x_pos in hud_items:
            lines = text.split("\n")
            for i, line in enumerate(lines):
                y_pos = 12 + (i * 18)
                sh_surf = hud_font.render(line, True, COLOR_BLACK)
                fg_surf = hud_font.render(
                    line,
                    True,
                    (255, 230, 80) if ("COINS" in line or (i == 1 and "TIME" in text and time_int <= 50)) else COLOR_WHITE
                )
                screen.blit(sh_surf, (x_pos + 1, y_pos + 1))
                screen.blit(fg_surf, (x_pos, y_pos))

        # 6. Pantalla de Victoria (Nivel Completado)
        if level.game_state == "VICTORY":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            vic_title = title_font.render("¡NIVEL COMPLETADO!", True, (255, 220, 50))
            vic_score = sub_font.render(f"PUNTUACIÓN FINAL: {player.score:06d}", True, COLOR_WHITE)
            vic_restart = guide_font.render("Presiona 'R' o ENTER para jugar de nuevo", True, (200, 255, 200))

            screen.blit(vic_title, vic_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 35)))
            screen.blit(vic_score, vic_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)))
            screen.blit(vic_restart, vic_restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 45)))

        # 7. Pantalla de Game Over
        elif level.game_state == "GAME_OVER":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            go_title = title_font.render("GAME OVER", True, (230, 40, 40))
            go_score = sub_font.render(f"PUNTUACIÓN FINAL: {player.score:06d}", True, COLOR_WHITE)
            go_restart = guide_font.render("Presiona 'R' o ENTER para reintentar la fase", True, (255, 200, 200))

            screen.blit(go_title, go_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 35)))
            screen.blit(go_score, go_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)))
            screen.blit(go_restart, go_restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 45)))

        # 8. Pantalla de Pausa
        elif is_paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            pause_title = title_font.render("JUEGO EN PAUSA", True, COLOR_WHITE)
            pause_sub = guide_font.render("Presiona ESC o P para reanudar", True, (220, 220, 220))
            screen.blit(pause_title, pause_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))
            screen.blit(pause_sub, pause_sub.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25)))

        # Guía inferior en juego activo
        else:
            tips_text = "Llega al Asta de la Bandera al final | LShift: Correr y Fuego | B: Super Mario | ESC/P: Pausa"
            t_sh = guide_font.render(tips_text, True, COLOR_BLACK)
            t_fg = guide_font.render(tips_text, True, (240, 240, 240))
            screen.blit(t_sh, (SCREEN_WIDTH // 2 - t_fg.get_width() // 2 + 1, SCREEN_HEIGHT - 21))
            screen.blit(t_fg, (SCREEN_WIDTH // 2 - t_fg.get_width() // 2, SCREEN_HEIGHT - 22))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

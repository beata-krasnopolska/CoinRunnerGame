from __future__ import annotations
import random
import pygame
from enemy import Enemy
from coin import Coin
from leaderboard import Leaderboard

from settings import (
    TIME_LIMIT_SECONDS, USE_TIME_LIMIT, WIDTH, HEIGHT, FPS,
    WHITE, BLACK, DARK_GRAY, GRAY, WIN_SCORE, YELLOW, RED,
    COIN_SIZE, COIN_VALUE,
    WIN_SCORE
)
from player import Player


class GameState:
    ENTER_NAME = "ENTER_NAME"
    START = "START"
    PLAYING = "PLAYING"
    GAME_OVER = "GAME_OVER"
    YOU_WIN = "YOU_WIN"


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()  # Inicjalizuj mixer do odtwarzania dźwięków
        pygame.display.set_caption("Coin Runner (pygame-ce)")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Załaduj dźwięk uderzenia gracza
        try:
            self.hit_sound = pygame.mixer.Sound(r"c:\Users\beata.krasnopolska\Downloads\playerhit.mp3")
        except pygame.error as e:
            print(f"Nie można załadować dźwięku: {e}")
            self.hit_sound = None

        self.world_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

        self.play_area = pygame.Rect(20, 60, WIDTH - 40, HEIGHT - 80)

        # Fonty (SysFont działa bez plików .ttf)
        self.font_big = pygame.font.SysFont(None, 72)
        self.font_med = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 26)

        self.state = GameState.ENTER_NAME  # Zacznij od wpisywania imienia
        self.start_ticks = 0
        self.elapsed_seconds = 0
        self.running = True
        self.lives = 3  # Liczba życ na początek
        self.invulnerable_time = 0  # Czas nieśmiertelności po utracie życia
        self.invulnerable_duration = 180  # 3 sekundy przy 60 FPS
        self.player_name = ""  # Imie gracza
        self.leaderboard = Leaderboard()  # Załaduj tablicę wyników

        self._new_run()

    def _new_run(self) -> None:
        """Reset całej rozgrywki (start nowej gry)."""
        self.score = 0
        self.lives = 3  # Reset życi na początek
        self.start_ticks = pygame.time.get_ticks()  # Zapisz czas startu rozgrywki
        self.elapsed_seconds = 0
        self.invulnerable_time = 0

        # Gracz startuje mniej więcej w lewym górnym rogu
        self.player = Player(60, 60)

        self.obstacles = self._build_obstacles()
        self.coin = self._spawn_coin()
        self.enemy = Enemy(700, 520, size=28, speed=3)

    def _build_obstacles(self) -> list[pygame.Rect]:
        """Prosta stała mapa przeszkód (możesz edytować)."""
        obstacles = [
            # Dwie długie "belki" z szerokimi przerwami (przejścia)
            pygame.Rect(60, 160, 250, 28),
            pygame.Rect(430, 160, 310, 28),

            pygame.Rect(60, 420, 310, 28),
            pygame.Rect(500, 420, 240, 28),

            # Pionowe ściany, ale nie domykają żadnego "pokoju"
            pygame.Rect(180, 220, 28, 140),
            pygame.Rect(600, 240, 28, 140),

            # Mała przeszkoda pośrodku (do omijania)
            pygame.Rect(360, 280, 80, 28),
        ]
        return obstacles

    def _spawn_coin(self) -> Coin:
        """Losuje pozycję monety tak, by nie kolidowała z przeszkodami ani graczem."""
        for _ in range(500):  # limit prób, żeby uniknąć pętli nieskończonej
            x = random.randint(20, WIDTH - COIN_SIZE - 20)
            y = random.randint(60, HEIGHT - COIN_SIZE - 20)  # 60 zostawiamy na HUD
            coin_rect = pygame.Rect(x, y, COIN_SIZE, COIN_SIZE)

            if coin_rect.colliderect(self.player.rect):
                continue
            if any(coin_rect.colliderect(obs) for obs in self.obstacles):
                continue

            return Coin(x, y)

        # Awaryjnie: jeśli coś pójdzie źle, daj monetę w stałym miejscu
        return Coin(700, 80)

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # na przyszłość; teraz nie jest potrzebne
            self._handle_events()
            self._update(dt)
            self._draw()

        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return

                if self.state == GameState.ENTER_NAME:
                    if event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if self.player_name.strip():
                            self.state = GameState.START
                    elif len(self.player_name) < 20:  # Limit długości imienia
                        if event.unicode.isprintable():
                            self.player_name += event.unicode

                elif self.state == GameState.START:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.PLAYING

                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        self._new_run()
                        self.state = GameState.PLAYING

                elif self.state == GameState.YOU_WIN:
                    if event.key == pygame.K_r:
                        self._new_run()
                        self.state = GameState.PLAYING

    def _update(self, dt: float) -> None:
        if self.state != GameState.PLAYING:
            return

        # Aktualizuj czas rozgrywki
        self.elapsed_seconds = (pygame.time.get_ticks() - self.start_ticks) // 1000

        # Aktualizuj animację monety
        self.coin.update()

        dx, dy = self.player.handle_input()
        self.player.move_and_collide(dx, dy, self.obstacles, self.world_rect)

        self.enemy.update(self.obstacles, self.play_area)

        # Zbieranie monety
        if self.player.rect.colliderect(self.coin):
            self.score += COIN_VALUE
            self.coin = self._spawn_coin()

        # YOU WIN — najpierw sprawdzamy zwycięstwo
        if self.score >= WIN_SCORE:
            # Zapisz wynik do tablicy
            self.leaderboard.add_score(self.player_name, self.score, self.elapsed_seconds)
            self.state = GameState.YOU_WIN
            return
        
        # Kolizja z wrogiem: utrata życia
        if self.invulnerable_time <= 0 and self.player.rect.colliderect(self.enemy.rect):
            self.lives -= 1
            self.invulnerable_time = self.invulnerable_duration
            
            # Odtwarzaj dźwięk uderzenia
            if self.hit_sound:
                self.hit_sound.play()
            
            if self.lives <= 0:
                # Zapisz wynik do tablicy
                self.leaderboard.add_score(self.player_name, self.score, self.elapsed_seconds)
                self.state = GameState.GAME_OVER
                return
        
        # Aktualizuj czas nieśmiertelności
        if self.invulnerable_time > 0:
            self.invulnerable_time -= 1

    def _draw(self) -> None:
        self.screen.fill(DARK_GRAY)

        if self.state == GameState.ENTER_NAME:
            self._draw_enter_name()
        elif self.state == GameState.START:
            self._draw_start()
        elif self.state == GameState.PLAYING:
            self._draw_playing()
        elif self.state == GameState.GAME_OVER:
            self._draw_game_over()
        elif self.state == GameState.YOU_WIN:
            self._draw_you_win()

        pygame.display.flip()

    def _draw_hud(self) -> None:
        # Pasek HUD
        pygame.draw.rect(self.screen, BLACK, pygame.Rect(0, 0, WIDTH, 50))
        name_surf = self.font_small.render(f"Gracz: {self.player_name}", True, YELLOW)
        score_surf = self.font_med.render(f"Score: {self.score}", True, WHITE)
        time_surf = self.font_med.render(f"Time: {self.elapsed_seconds}s", True, WHITE)
        lives_surf = self.font_med.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(name_surf, (20, 2))
        self.screen.blit(score_surf, (20, 20))
        self.screen.blit(time_surf, (WIDTH - 220, 12))
        self.screen.blit(lives_surf, (WIDTH // 2 - 50, 12))

    def _draw_playing(self) -> None:
        self._draw_hud()

        # Przeszkody
        for obs in self.obstacles:
            pygame.draw.rect(self.screen, GRAY, obs)

        # Moneta
        self.coin.draw(self.screen)

        # Wróg
        self.enemy.draw(self.screen, RED)

        # Gracz (przekaż informację o nieśmiertelności)
        is_invulnerable = self.invulnerable_time > 0
        self.player.draw(self.screen, is_invulnerable)

    def _draw_center_text(self, text: str, y: int, font: pygame.font.Font, color: tuple[int, int, int]) -> None:
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(WIDTH // 2, y))
        self.screen.blit(surf, rect)

    def _draw_leaderboard(self, start_y: int) -> None:
        """Rysuj tablicę wyników"""
        scores = self.leaderboard.get_top_scores(5)
        
        # Nagłówek
        header_text = self.font_small.render("TOP 5 WYNIKI", True, YELLOW)
        header_rect = header_text.get_rect(center=(WIDTH // 2, start_y))
        self.screen.blit(header_text, header_rect)
        
        # Wyniki
        y_offset = start_y + 30
        for idx, score in enumerate(scores, 1):
            score_text = f"{idx}. {score.name:<12} Pkt: {score.points:<3} Czas: {score.time}s"
            score_surf = self.font_small.render(score_text, True, WHITE)
            self.screen.blit(score_surf, (WIDTH // 2 - 150, y_offset))
            y_offset += 25

    def _draw_enter_name(self) -> None:
        self._draw_center_text("COIN RUNNER", 120, self.font_big, WHITE)
        self._draw_center_text("Wpisz swoje imie:", 220, self.font_med, WHITE)
        
        # Rysuj pole do wpisywania z kursorem
        input_box = pygame.Rect(WIDTH // 2 - 150, 280, 300, 50)
        pygame.draw.rect(self.screen, WHITE, input_box, 2)
        
        # Wyświetl wpisane imię
        name_surf = self.font_med.render(self.player_name, True, WHITE)
        self.screen.blit(name_surf, (input_box.x + 10, input_box.y + 8))
        
        # Kursor
        if (pygame.time.get_ticks() // 500) % 2:  # Miganie kursora
            cursor_x = input_box.x + 10 + name_surf.get_width()
            pygame.draw.line(self.screen, WHITE, (cursor_x, input_box.y + 5), (cursor_x, input_box.y + 45), 2)
        
        self._draw_center_text("ENTER - start", 420, self.font_small, YELLOW)

    def _draw_start(self) -> None:
        self._draw_center_text("COIN RUNNER", 180, self.font_big, WHITE)
        self._draw_center_text("Ruch: WASD / Strzalki", 280, self.font_med, WHITE)
        self._draw_center_text("Zbieraj monety: +10", 320, self.font_med, WHITE)
        self._draw_center_text("START: SPACJA", 400, self.font_med, YELLOW)
        self._draw_center_text("Wyjscie: ESC", 440, self.font_small, WHITE)

    def _draw_game_over(self) -> None:
        self._draw_center_text("GAME OVER", 80, self.font_big, RED)
        self._draw_center_text(f"Gracz: {self.player_name}", 140, self.font_med, YELLOW)
        self._draw_center_text(f"Twoj wynik: {self.score} | Czas: {self.elapsed_seconds}s", 190, self.font_small, WHITE)
        
        # Rysuj tablicę wyników
        self._draw_leaderboard(240)
        
        self._draw_center_text("R - restart", 520, self.font_med, YELLOW)
        self._draw_center_text("ESC - wyjscie", 560, self.font_small, WHITE)

    def _draw_you_win(self) -> None:
        self._draw_center_text("YOU WIN!", 80, self.font_big, YELLOW)
        self._draw_center_text(f"Gracz: {self.player_name}", 140, self.font_med, YELLOW)
        self._draw_center_text(f"Wynik: {self.score} | Czas: {self.elapsed_seconds}s", 190, self.font_small, WHITE)
        
        # Rysuj tablicę wyników
        self._draw_leaderboard(240)
        
        self._draw_center_text("R - restart", 520, self.font_med, YELLOW)
        self._draw_center_text("ESC - wyjscie", 560, self.font_small, WHITE)
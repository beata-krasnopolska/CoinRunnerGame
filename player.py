from __future__ import annotations
import math
import pygame
from settings import PLAYER_SIZE, PLAYER_SPEED, GREEN


class Player:
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.speed = PLAYER_SPEED

    def handle_input(self) -> tuple[int, int]:
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        # Normalizacja wektora kierunku
        if dx != 0 or dy != 0:
            magnitude = math.sqrt(dx**2 + dy**2)
            dx = int((dx / magnitude) * self.speed)
            dy = int((dy / magnitude) * self.speed)

        return dx, dy

    def move_and_collide(self, dx: int, dy: int, obstacles: list[pygame.Rect], world_rect: pygame.Rect) -> None:
        # Ruch w osi X + kolizje
        if dx != 0:
            self.rect.x += dx
            self._resolve_collisions(obstacles, axis="x")

        # Ruch w osi Y + kolizje
        if dy != 0:
            self.rect.y += dy
            self._resolve_collisions(obstacles, axis="y")

        # Trzymaj gracza w granicach ekranu
        self.rect.clamp_ip(world_rect)

    def _resolve_collisions(self, obstacles: list[pygame.Rect], axis: str) -> None:
        for obs in obstacles:
            if self.rect.colliderect(obs):
                if axis == "x":
                    if self.rect.centerx > obs.centerx:
                        self.rect.left = obs.right
                    else:
                        self.rect.right = obs.left
                else:  # axis == "y"
                    if self.rect.centery > obs.centery:
                        self.rect.top = obs.bottom
                    else:
                        self.rect.bottom = obs.top

    def draw(self, screen: pygame.Surface, is_invulnerable: bool = False) -> None:
        # Określ kolor na podstawie stanu nieśmiertelności
        if is_invulnerable:
            # Migający efekt - żółty/jasny kolor gdy nieśmiertelny
            body_color = (255, 255, 100)  # Jasny żółty
            head_color = (255, 255, 100)
        else:
            body_color = GREEN
            head_color = GREEN
        
        # Ciało (prostokąt)
        body_rect = pygame.Rect(self.rect.x + 6, self.rect.y + 10, 20, 16)
        pygame.draw.rect(screen, body_color, body_rect)
        
        # Głowa (okrąg)
        head_center = (self.rect.centerx, self.rect.y + 6)
        pygame.draw.circle(screen, head_color, head_center, 6)
        
        # Oczy
        pygame.draw.circle(screen, (0, 0, 0), (head_center[0] - 3, head_center[1] - 1), 1)
        pygame.draw.circle(screen, (0, 0, 0), (head_center[0] + 3, head_center[1] - 1), 1)
from __future__ import annotations
import pygame

class Enemy:
    def __init__(self, x: int, y: int, size: int = 28, speed: int = 3):
        self.rect = pygame.Rect(x, y, size, size)
        self.vx = speed
        self.vy = speed

    def update(self, obstacles: list[pygame.Rect], world_rect: pygame.Rect) -> None:
        # Ruch X
        self.rect.x += self.vx
        if not world_rect.contains(self.rect) or any(self.rect.colliderect(o) for o in obstacles):
            self.rect.x -= self.vx
            self.vx *= -1
            self.rect.x += self.vx  # spróbuj w drugą stronę

        # Ruch Y
        self.rect.y += self.vy
        if not world_rect.contains(self.rect) or any(self.rect.colliderect(o) for o in obstacles):
            self.rect.y -= self.vy
            self.vy *= -1
            self.rect.y += self.vy

        # Na pewno w granicach świata
        self.rect.clamp_ip(world_rect)

    def draw(self, screen: pygame.Surface, color: tuple[int, int, int]) -> None:
        pygame.draw.rect(screen, color, self.rect)
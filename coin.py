from __future__ import annotations
import pygame
import os
from settings import COIN_SIZE


class Coin:
    """Animowana moneta używająca obrazków z folderu spinning_coin"""
    
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, COIN_SIZE, COIN_SIZE)
        self.x = x
        self.y = y
        
        # Załaduj wszystkie klatki animacji
        self.frames = self._load_frames()
        self.current_frame = 0
        self.animation_speed = 2  # co ile klatek zmienić obrazek (niska liczba = szybsza animacja)
        self.frame_counter = 0
        
        # Pobierz pierwszą klatkę
        if self.frames:
            self.image = self.frames[0]
        else:
            self.image = None

    def _load_frames(self) -> list[pygame.Surface]:
        """Załaduj wszystkie klatki monety z folderu spinning_coin"""
        frames = []
        coin_dir = os.path.join(os.path.dirname(__file__), "spinning_coin")
        
        # Załaduj obrazki od coin1.png do coin10.png
        for i in range(1, 11):
            filename = f"coin{i}.png"
            filepath = os.path.join(coin_dir, filename)
            
            if os.path.exists(filepath):
                try:
                    img = pygame.image.load(filepath)
                    # Przeskaluj do rozmiaru COIN_SIZE
                    img = pygame.transform.scale(img, (COIN_SIZE, COIN_SIZE))
                    frames.append(img)
                except pygame.error as e:
                    print(f"Nie można załadować {filename}: {e}")
            else:
                print(f"Plik nie znaleziony: {filepath}")
        
        if not frames:
            print("Ostrzeżenie: Nie załadowano żadnych klatek monety!")
        
        return frames

    def update(self) -> None:
        """Aktualizuj animację monety"""
        if not self.frames:
            return
        
        self.frame_counter += 1
        
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
        
        # Aktualizuj rect na wypadek przesunięcia
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, screen: pygame.Surface) -> None:
        """Rysuj bieżącą klatkę monety"""
        if self.image:
            screen.blit(self.image, self.rect)

    def move(self, dx: int, dy: int) -> None:
        """Przesunięcie monety"""
        self.x += dx
        self.y += dy

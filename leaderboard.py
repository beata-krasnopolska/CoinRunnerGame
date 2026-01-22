from __future__ import annotations
import json
import os
from dataclasses import dataclass


@dataclass
class Score:
    """Pojedynczy wynik gracza"""
    name: str
    points: int
    time: int  # czas w sekundach
    
    def to_dict(self) -> dict:
        return {"name": self.name, "points": self.points, "time": self.time}
    
    @staticmethod
    def from_dict(data: dict) -> Score:
        return Score(data["name"], data["points"], data["time"])


class Leaderboard:
    """Zarządzanie tablicą wyników"""
    
    def __init__(self, filename: str = "leaderboard.json"):
        self.filename = filename
        self.scores: list[Score] = []
        self._load()
    
    def _load(self) -> None:
        """Załaduj wyniki z pliku"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.scores = [Score.from_dict(item) for item in data]
            except (json.JSONDecodeError, KeyError):
                self.scores = []
        else:
            self.scores = []
    
    def _save(self) -> None:
        """Zapisz wyniki do pliku"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            data = [score.to_dict() for score in self.scores]
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_score(self, name: str, points: int, time: int) -> None:
        """Dodaj nowy wynik"""
        self.scores.append(Score(name, points, time))
        # Sortuj: najpierw po punktach (malejąco), potem po czasie (rosnąco)
        self.scores.sort(key=lambda s: (-s.points, s.time))
        # Zachowaj top 10
        self.scores = self.scores[:10]
        self._save()
    
    def get_top_scores(self, limit: int = 10) -> list[Score]:
        """Pobierz najlepsze wyniki"""
        return self.scores[:limit]
    
    def is_high_score(self, points: int, time: int = None) -> int:
        """Sprawdź czy wynik trafia do top 10, zwróć pozycję (-1 jeśli nie)"""
        if len(self.scores) < 10:
            return len(self.scores)
        
        # Sprawdź czy przebija najmniejszy wynik w top 10
        last_score = self.scores[-1]
        if points > last_score.points:
            return 9
        elif points == last_score.points and time is not None and time < last_score.time:
            return 9
        
        return -1
    
    def clear(self) -> None:
        """Wyczyść tablicę wyników"""
        self.scores = []
        self._save()

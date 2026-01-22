# Coin Runner Game

A fun and engaging 2D arcade-style game built with **Pygame** where players collect coins while avoiding enemies.

## Overview

Coin Runner is a classic arcade game where your objective is to collect as many coins as possible while avoiding moving enemies. Navigate your character around the game board, grab coins for points, and compete for the highest score!

## Features

- **Player Character**: Control a green square character with keyboard controls
- **Coins**: Collect coins scattered across the game board to earn points
- **Enemies**: Avoid red enemy squares that patrol the game area
- **Scoring System**: Each coin collected adds to your score (10 points per coin)
- **Win Condition**: Reach 100 points to win the game
- **Leaderboard**: Track high scores and player rankings
- **Player Name Entry**: Enter your name before starting to be recorded on the leaderboard
- **Sound Effects**: Includes audio feedback when the player is hit by an enemy
- **Time Limit Option**: Optional game mode with a 60-second time limit

## Game Controls

| Key | Action |
|-----|--------|
| **Arrow Keys** or **WASD** | Move the player |
| **Q** or **ESC** | Quit the game |

## Installation

1. Make sure you have Python 3.8+ installed
2. Install the required dependencies:

```bash
pip install pygame
```

## How to Play

1. Run the game:
```bash
python main.py
```

2. Enter your player name when prompted
3. Use arrow keys or WASD to move your character
4. Collect coins (yellow squares) to increase your score
5. Avoid enemies (red squares) - touching them will damage you
6. Reach 100 points to win!
7. Your score will be saved to the leaderboard

## Game Settings

You can customize the game behavior by editing `settings.py`:

- **WIDTH / HEIGHT**: Game window dimensions (default: 800x600)
- **FPS**: Frames per second (default: 60)
- **WIN_SCORE**: Points needed to win (default: 100)
- **TIME_LIMIT_SECONDS**: Time limit in seconds (default: 60)
- **USE_TIME_LIMIT**: Enable/disable time limit mode (default: False)
- **PLAYER_SIZE**: Player character size (default: 32)
- **PLAYER_SPEED**: Player movement speed (default: 6)
- **COIN_SIZE**: Coin size (default: 20)
- **COIN_VALUE**: Points per coin (default: 10)

## Project Structure

- `main.py` - Entry point for the game
- `game.py` - Core game logic and state management
- `player.py` - Player character class
- `enemy.py` - Enemy character class
- `coin.py` - Coin collectible class
- `leaderboard.py` - Leaderboard management and persistence
- `settings.py` - Game configuration and constants
- `test_game.py` - Unit tests for game functionality

## Dependencies

- **pygame** - Game development library
- **Python 3.8+**

## Notes

- Sound files may need to be configured based on your system setup
- The game uses system fonts (no external font files required)
- Leaderboard data is stored in `leaderboard.json`

## Author

Created as a Python learning project for game development basics.

---

Enjoy playing Coin Runner! 🎮

import unittest
import pygame
from player import Player
from settings import PLAYER_SIZE, PLAYER_SPEED, WIDTH, HEIGHT, COIN_SIZE, COIN_VALUE, WIN_SCORE


class TestPlayer(unittest.TestCase):
    """Tests for Player class"""

    def setUp(self):
        """Inicjalization pygame before each test"""
        pygame.init()

    def tearDown(self):
        """Cleanup pygame after each test"""
        pygame.quit()

    def test_player_initialization(self):
        """Player initialization test"""
        player = Player(60, 60)
        self.assertEqual(player.rect.x, 60)
        self.assertEqual(player.rect.y, 60)
        self.assertEqual(player.rect.width, PLAYER_SIZE)
        self.assertEqual(player.rect.height, PLAYER_SIZE)
        self.assertEqual(player.speed, PLAYER_SPEED)

    def test_player_position(self):
        """Test player position in various locations"""
        positions = [(10, 20), (100, 150), (700, 500)]
        for x, y in positions:
            player = Player(x, y)
            self.assertEqual(player.rect.x, x)
            self.assertEqual(player.rect.y, y)

    def test_handle_input_no_movement(self):
        """Test handle_input with no keys pressed"""
        player = Player(100, 100)
        dx, dy = player.handle_input()
        self.assertEqual(dx, 0)
        self.assertEqual(dy, 0)

    def test_player_boundaries(self):
        """Test if player stays within world boundaries"""
        player = Player(50, 50)
        world_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        
        # Try to move player outside the left and top boundaries
        player.rect.x = -10
        player.move_and_collide(0, 0, [], world_rect)
        self.assertGreaterEqual(player.rect.x, 0)
        
        player.rect.y = -10
        player.move_and_collide(0, 0, [], world_rect)
        self.assertGreaterEqual(player.rect.y, 0)

    def test_collision_with_obstacle_x_axis(self):
        """Tests of player collision with an obstacle on the X axis"""
        player = Player(100, 100)
        obstacle = pygame.Rect(150, 90, 40, 60)
        world_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        
        # Player moved to the right towards the obstacle
        player.move_and_collide(60, 0, [obstacle], world_rect)
        
        # Player should stop before the obstacle
        self.assertLess(player.rect.right, obstacle.left + 5)

    def test_collision_with_obstacle_y_axis(self):
        """Tests of player collision with an obstacle on the Y axis"""
        player = Player(100, 100)
        obstacle = pygame.Rect(90, 150, 60, 40)
        world_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        
        # Player moved down towards the obstacle
        player.move_and_collide(0, 60, [obstacle], world_rect)
        
        # Player should stop before the obstacle
        self.assertLess(player.rect.bottom, obstacle.top + 5)

    def test_move_without_obstacles(self):
        """Test move without obstacles"""
        player = Player(100, 100)
        world_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        
        initial_x = player.rect.x
        player.move_and_collide(20, 0, [], world_rect)
        
        self.assertEqual(player.rect.x, initial_x + 20)

    def test_multiple_obstacles(self):
        """Test move with multiple obstacles"""
        player = Player(100, 100)
        obstacles = [
            pygame.Rect(150, 90, 40, 60),
            pygame.Rect(200, 100, 30, 30),
            pygame.Rect(90, 150, 60, 40)
        ]
        world_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        
        player.move_and_collide(100, 60, obstacles, world_rect)
        
        # Player should be somewhere in a safe place
        self.assertGreater(player.rect.x, 0)
        self.assertGreater(player.rect.y, 0)
        self.assertLess(player.rect.right, WIDTH)
        self.assertLess(player.rect.bottom, HEIGHT)


class TestSettings(unittest.TestCase):
    """Testy config values from settings.py"""

    def test_player_size_positive(self):
        """Test if player size is positive"""
        self.assertGreater(PLAYER_SIZE, 0)

    def test_player_speed_positive(self):
        """Test if player speed is positive"""
        self.assertGreater(PLAYER_SPEED, 0)

    def test_coin_size_positive(self):
        """Test if coin size is positive"""
        self.assertGreater(COIN_SIZE, 0)

    def test_coin_value_positive(self):
        """Test if coin value is positive"""
        self.assertGreater(COIN_VALUE, 0)

    def test_win_score_positive(self):
        """Test if required win score is positive"""
        self.assertGreater(WIN_SCORE, 0)

    def test_screen_dimensions_positive(self):
        """Test if screen dimensions are positive"""
        self.assertGreater(WIDTH, 0)
        self.assertGreater(HEIGHT, 0)

    def test_coin_value_less_than_win_score(self):
        """Test if coin value is less than win score"""
        self.assertLess(COIN_VALUE, WIN_SCORE)


class TestGameLogic(unittest.TestCase):
    """Testy for game logic"""

    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_coins_needed_to_win(self):
        """Test how many collect to win the game"""
        coins_needed = WIN_SCORE // COIN_VALUE
        self.assertEqual(coins_needed * COIN_VALUE, WIN_SCORE)

    def test_player_rect_collision_detection(self):
        """Test to collision detection between player and coin"""
        player = Player(100, 100)
        coin = pygame.Rect(100, 100, COIN_SIZE, COIN_SIZE)
        
        # Should collied (the same position)
        self.assertTrue(player.rect.colliderect(coin))

    def test_player_rect_no_collision(self):
        """Test no collision when objects are far apart"""
        player = Player(100, 100)
        coin = pygame.Rect(500, 500, COIN_SIZE, COIN_SIZE)
        
        # Should not collide
        self.assertFalse(player.rect.colliderect(coin))


if __name__ == '__main__':
    unittest.main()

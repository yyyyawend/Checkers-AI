"""
Constant parameters for pygame.
"""
import pygame

WIDTH, HEIGHT = 400, 400
ROWS = 4
COLS = 4
SQUARE_SIZE = HEIGHT // ROWS

BLUE = (255, 211, 155)
RED = (205, 170, 125)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
YELLOW = (0, 128, 128)
GREEN = (100, 149, 237)
GREY = (128,128,128)
CROWN = pygame.transform.scale(pygame.image.load('checkers/assets/crown.png'), (25, 15))

"""
Constants and configuration for Rock Paper Scissors Arena.
"""

import pygame
from enum import Enum

# Screen setup
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 900

# Colors - Vibrant arcade palette
COLORS = {
    'bg_dark': (15, 15, 25),
    'bg_gradient': (25, 20, 45),
    'white': (255, 255, 255),
    'gold': (255, 215, 0),
    'silver': (192, 192, 192),
    'red': (255, 70, 70),
    'green': (70, 255, 120),
    'blue': (70, 150, 255),
    'purple': (180, 100, 255),
    'orange': (255, 165, 0),
    'cyan': (0, 255, 255),
    'pink': (255, 105, 180),
    'yellow': (255, 255, 100),
    'lime': (180, 255, 100),
    'teal': (100, 255, 220),
}

# Player colors for 8 players
PLAYER_COLORS = [
    (255, 70, 70),    # Red
    (70, 150, 255),   # Blue
    (70, 255, 120),   # Green
    (255, 215, 0),    # Gold
    (180, 100, 255),  # Purple
    (255, 165, 0),    # Orange
    (0, 255, 255),    # Cyan
    (255, 105, 180),  # Pink
]


class Choice(Enum):
    """Player choice in rock paper scissors."""
    NONE = 0
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class SceneType(Enum):
    """Game scene types."""
    MENU = 1
    GAME = 2
    RESOLUTION = 3
    VICTORY = 4


# Initialize fonts (call after pygame.init())
FONT_LARGE = None
FONT_MEDIUM = None
FONT_SMALL = None
FONT_TINY = None


def init_fonts():
    """Initialize fonts after pygame is initialized."""
    global FONT_LARGE, FONT_MEDIUM, FONT_SMALL, FONT_TINY
    try:
        FONT_LARGE = pygame.font.Font(None, 120)
        FONT_MEDIUM = pygame.font.Font(None, 60)
        FONT_SMALL = pygame.font.Font(None, 36)
        FONT_TINY = pygame.font.Font(None, 28)
    except:
        FONT_LARGE = pygame.font.SysFont('arial', 100)
        FONT_MEDIUM = pygame.font.SysFont('arial', 48)
        FONT_SMALL = pygame.font.SysFont('arial', 30)
        FONT_TINY = pygame.font.SysFont('arial', 22)


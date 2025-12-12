"""
Background rendering for Rock Paper Scissors Arena.
"""

import pygame

from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from config.colors import COLORS


def draw_gradient_bg(surface: pygame.Surface):
    """Draw a gradient background."""
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(COLORS['bg_dark'][0] * (1 - ratio) + COLORS['bg_gradient'][0] * ratio)
        g = int(COLORS['bg_dark'][1] * (1 - ratio) + COLORS['bg_gradient'][1] * ratio)
        b = int(COLORS['bg_dark'][2] * (1 - ratio) + COLORS['bg_gradient'][2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))


def create_background_surface() -> pygame.Surface:
    """Create and return a pre-rendered background surface."""
    bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    draw_gradient_bg(bg_surface)
    return bg_surface


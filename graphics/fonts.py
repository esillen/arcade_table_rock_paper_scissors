"""
Font management for Rock Paper Scissors Arena.
"""

import pygame

# Font storage
_fonts = {
    'large': None,
    'medium': None,
    'small': None,
    'tiny': None,
}


def init_fonts():
    """Initialize fonts after pygame is initialized."""
    global _fonts
    try:
        _fonts['large'] = pygame.font.Font(None, 120)
        _fonts['medium'] = pygame.font.Font(None, 60)
        _fonts['small'] = pygame.font.Font(None, 36)
        _fonts['tiny'] = pygame.font.Font(None, 28)
    except:
        _fonts['large'] = pygame.font.SysFont('arial', 100)
        _fonts['medium'] = pygame.font.SysFont('arial', 48)
        _fonts['small'] = pygame.font.SysFont('arial', 30)
        _fonts['tiny'] = pygame.font.SysFont('arial', 22)


def get_font(size: str) -> pygame.font.Font:
    """
    Get a font by size name.
    
    Args:
        size: One of 'large', 'medium', 'small', 'tiny'
    
    Returns:
        The pygame Font object
    """
    return _fonts.get(size)


# Convenience accessors
def font_large() -> pygame.font.Font:
    return _fonts['large']

def font_medium() -> pygame.font.Font:
    return _fonts['medium']

def font_small() -> pygame.font.Font:
    return _fonts['small']

def font_tiny() -> pygame.font.Font:
    return _fonts['tiny']


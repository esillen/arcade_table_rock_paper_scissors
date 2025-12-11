"""
Base scene class for Rock Paper Scissors Arena.
"""

import pygame
from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from player import Player

from constants import SceneType


class Scene(ABC):
    """Abstract base class for all game scenes."""
    
    def __init__(self, screen: pygame.Surface, bg_surface: pygame.Surface):
        self.screen = screen
        self.bg_surface = bg_surface
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event, players: List['Player']) -> Optional[SceneType]:
        """
        Handle a pygame event.
        Returns a SceneType if scene should change, None otherwise.
        """
        pass
    
    @abstractmethod
    def update(self, players: List['Player']) -> Optional[SceneType]:
        """
        Update scene state.
        Returns a SceneType if scene should change, None otherwise.
        """
        pass
    
    @abstractmethod
    def draw(self, players: List['Player']):
        """Draw the scene."""
        pass
    
    def draw_background(self):
        """Draw the pre-rendered background."""
        self.screen.blit(self.bg_surface, (0, 0))


"""
Victory scene for Rock Paper Scissors Arena.
"""

import pygame
import math
from typing import List, Optional

from scenes.base import Scene
from core.enums import SceneType
from core.player import Player
from core.rules import get_winner
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from config.colors import COLORS, PLAYER_COLORS
from graphics.fonts import font_large, font_medium


class VictoryScene(Scene):
    """Victory scene celebrating the winner."""
    
    def __init__(self, screen: pygame.Surface, bg_surface: pygame.Surface):
        super().__init__(screen, bg_surface)
        self.winner: Optional[Player] = None
    
    def set_winner(self, players: List[Player]):
        """Find and set the winner from the player list."""
        self.winner = get_winner(players)
    
    def handle_event(self, event: pygame.event.Event, players: List[Player]) -> Optional[SceneType]:
        """Handle victory input events."""
        if event.type != pygame.KEYDOWN:
            return None
        
        if event.key == pygame.K_SPACE:
            return SceneType.MENU
        
        return None
    
    def update(self, players: List[Player]) -> Optional[SceneType]:
        """Update victory state (nothing to update)."""
        return None
    
    def draw(self, players: List[Player]):
        """Draw the victory scene."""
        self.draw_background()
        
        # Animated background particles
        time = pygame.time.get_ticks() / 1000
        for i in range(20):
            px = (SCREEN_WIDTH // 2 + math.sin(time * 2 + i) * (200 + i * 20)) % SCREEN_WIDTH
            py = (SCREEN_HEIGHT // 2 + math.cos(time * 2 + i * 0.5) * (150 + i * 15)) % SCREEN_HEIGHT
            color = PLAYER_COLORS[i % len(PLAYER_COLORS)]
            pygame.draw.circle(self.screen, color, (int(px), int(py)), 5 + i % 5)
        
        if self.winner:
            # Winner announcement
            winner_text = font_large().render(f"PLAYER {self.winner.id} WINS!", True, self.winner.color)
            winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            self.screen.blit(winner_text, winner_rect)
            
            # Trophy/celebration
            trophy_text = font_large().render("🏆", True, COLORS['gold'])
            trophy_rect = trophy_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(trophy_text, trophy_rect)
            
            # Draw large player icon
            pygame.draw.circle(self.screen, self.winner.color, 
                             (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20), 80, 8)
        else:
            # No winner (everyone eliminated somehow)
            draw_text = font_large().render("NOBODY WINS!", True, COLORS['red'])
            draw_rect = draw_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(draw_text, draw_rect)
        
        # Restart prompt
        restart = font_medium().render("Press SPACE for new game", True, COLORS['white'])
        restart_rect = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        self.screen.blit(restart, restart_rect)

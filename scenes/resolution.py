"""
Resolution scene for Rock Paper Scissors Arena.
"""

import pygame
from typing import List, Optional

from scenes.base import Scene
import constants
from constants import SceneType, COLORS, SCREEN_WIDTH, SCREEN_HEIGHT
from graphics import draw_player_slot
from player import Player, get_alive_count


class ResolutionScene(Scene):
    """Resolution scene showing round results."""
    
    def __init__(self, screen: pygame.Surface, bg_surface: pygame.Surface):
        super().__init__(screen, bg_surface)
        self.eliminated_this_round: List[Player] = []
    
    def set_eliminated(self, eliminated: List[Player]):
        """Set the list of eliminated players for display."""
        self.eliminated_this_round = eliminated
    
    def handle_event(self, event: pygame.event.Event, players: List[Player]) -> Optional[SceneType]:
        """Handle resolution input events."""
        if event.type != pygame.KEYDOWN:
            return None
        
        if event.key == pygame.K_SPACE:
            alive_count = get_alive_count(players)
            if alive_count <= 1:
                return SceneType.VICTORY
            else:
                return SceneType.GAME
        
        return None
    
    def update(self, players: List[Player]) -> Optional[SceneType]:
        """Update resolution state (nothing to update)."""
        return None
    
    def draw(self, players: List[Player]):
        """Draw the resolution scene."""
        self.draw_background()
        
        # Title
        title = constants.FONT_LARGE.render("RESULTS", True, COLORS['gold'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(title, title_rect)
        
        # Show elimination status
        if self.eliminated_this_round:
            elim_names = ", ".join([f"P{p.id}" for p in self.eliminated_this_round])
            elim_text = constants.FONT_MEDIUM.render(f"ELIMINATED: {elim_names}", True, COLORS['red'])
        else:
            elim_text = constants.FONT_MEDIUM.render("DRAW! No eliminations", True, COLORS['cyan'])
        elim_rect = elim_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(elim_text, elim_rect)
        
        # Continue prompt
        alive = get_alive_count(players)
        if alive <= 1:
            cont_text = "Press SPACE to see the winner!"
        else:
            cont_text = f"Press SPACE to continue ({alive} players remaining)"
        cont = constants.FONT_SMALL.render(cont_text, True, COLORS['green'])
        cont_rect = cont.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(cont, cont_rect)
        
        # Draw player slots with choices revealed
        for player in players:
            if player.joined:
                draw_player_slot(self.screen, player, show_choice=True, show_controls=False)


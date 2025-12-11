"""
Game scene for Rock Paper Scissors Arena.
"""

import pygame
from typing import List, Optional

from scenes.base import Scene
import constants
from constants import SceneType, COLORS, SCREEN_WIDTH, SCREEN_HEIGHT
from graphics import draw_player_slot
from player import Player


class GameScene(Scene):
    """Game scene where players choose rock, paper, or scissors."""
    
    def __init__(self, screen: pygame.Surface, bg_surface: pygame.Surface):
        super().__init__(screen, bg_surface)
        self.countdown_duration = 3  # seconds
        self.countdown_start = 0
        self.round_number = 1
    
    def start_countdown(self):
        """Start the countdown timer."""
        self.countdown_start = pygame.time.get_ticks()
    
    def reset_round(self):
        """Reset for a new round."""
        self.round_number += 1
        self.start_countdown()
    
    def reset_game(self):
        """Reset for a completely new game."""
        self.round_number = 1
        self.start_countdown()
    
    def get_remaining_time(self) -> float:
        """Get remaining countdown time in seconds."""
        elapsed = (pygame.time.get_ticks() - self.countdown_start) / 1000
        return max(0, self.countdown_duration - elapsed)
    
    def handle_event(self, event: pygame.event.Event, players: List[Player]) -> Optional[SceneType]:
        """Handle game input events."""
        if event.type != pygame.KEYDOWN:
            return None
        
        # Let players make their choices
        for player in players:
            if player.joined and player.alive:
                player.handle_input(event.key)
        
        return None
    
    def update(self, players: List[Player]) -> Optional[SceneType]:
        """Update game state."""
        if self.get_remaining_time() <= 0:
            # Time's up - go to resolution
            return SceneType.RESOLUTION
        return None
    
    def draw(self, players: List[Player]):
        """Draw the game scene."""
        self.draw_background()
        
        remaining = self.get_remaining_time()
        
        if remaining > 0:
            # Countdown number
            countdown_num = int(remaining) + 1
            countdown_text = constants.FONT_LARGE.render(str(countdown_num), True, COLORS['gold'])
            countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(countdown_text, countdown_rect)
            
            # Instructions
            choose_text = constants.FONT_MEDIUM.render("CHOOSE YOUR WEAPON!", True, COLORS['white'])
            choose_rect = choose_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            self.screen.blit(choose_text, choose_rect)
        
        # Round indicator
        round_text = constants.FONT_SMALL.render(f"Round {self.round_number}", True, COLORS['silver'])
        round_rect = round_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(round_text, round_rect)
        
        # Draw player slots
        for player in players:
            if player.joined:
                draw_player_slot(self.screen, player, show_choice=False, show_controls=True)


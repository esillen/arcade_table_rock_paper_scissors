"""
Menu scene for Rock Paper Scissors Arena.
"""

import pygame
from typing import List, Optional

from scenes.base import Scene
from core.enums import SceneType, Choice
from core.rules import get_joined_count
from core.player import Player
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from config.colors import COLORS
from graphics.fonts import font_large, font_medium, font_small
from graphics.player_slot import draw_player_slot


class MenuScene(Scene):
    """Main menu scene where players can join the game."""
    
    def handle_event(self, event: pygame.event.Event, players: List[Player]) -> Optional[SceneType]:
        """Handle menu input events."""
        if event.type != pygame.KEYDOWN:
            return None
        
        # Check for player ready (left/rock key) or unready (right/scissors key)
        for player in players:
            if event.key == player.rock_key:
                player.joined = True
            elif event.key == player.scissors_key:
                player.joined = False
        
        # Start game with space if enough players
        if event.key == pygame.K_SPACE and get_joined_count(players) >= 2:
            # Initialize players for game
            for player in players:
                player.alive = player.joined
            return SceneType.GAME
        
        return None
    
    def update(self, players: List[Player]) -> Optional[SceneType]:
        """Update menu state (nothing to update)."""
        return None
    
    def draw(self, players: List[Player]):
        """Draw the menu scene."""
        self.draw_background()
        
        # Title
        title = font_large().render("ROCK PAPER SCISSORS", True, COLORS['gold'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(title, title_rect)
        
        subtitle = font_medium().render("ARENA", True, COLORS['cyan'])
        sub_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(subtitle, sub_rect)
        
        # Instructions
        joined = get_joined_count(players)
        if joined < 2:
            inst_text = f"Need {2 - joined} more player(s) to start"
            inst_color = COLORS['orange']
        else:
            inst_text = "Press SPACE to start!"
            inst_color = COLORS['green']
        
        inst = font_small().render(inst_text, True, inst_color)
        inst_rect = inst.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(inst, inst_rect)
        
        # Player count
        count_text = font_small().render(f"Players: {joined}/8", True, COLORS['white'])
        count_rect = count_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(count_text, count_rect)
        
        # Draw player slots (only show players who haven't joined yet or are still alive)
        for player in players:
            if not player.joined or player.alive:
                draw_player_slot(self.screen, player, show_choice=False, show_controls=False)

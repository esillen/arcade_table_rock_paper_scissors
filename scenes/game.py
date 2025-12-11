"""
Game scene for Rock Paper Scissors Arena.
"""

import pygame
import math
from typing import List, Optional

from scenes.base import Scene
import constants
from constants import SceneType, COLORS, Choice, SCREEN_WIDTH, SCREEN_HEIGHT
from graphics import draw_player_slot
from player import Player


class GameScene(Scene):
    """Game scene where players choose rock, paper, or scissors."""
    
    def __init__(self, screen: pygame.Surface, bg_surface: pygame.Surface):
        super().__init__(screen, bg_surface)
        self.countdown_duration = 10  # seconds
        self.countdown_start = 0
        self.round_number = 1
        self.speedup_triggered = False
        self.speedup_time = 0  # When speedup was triggered
        self.time_at_speedup = 0  # Remaining time when speedup happened
    
    def start_countdown(self):
        """Start the countdown timer."""
        self.countdown_start = pygame.time.get_ticks()
        self.speedup_triggered = False
        self.speedup_time = 0
        self.time_at_speedup = 0
    
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
        if self.speedup_triggered:
            # Calculate time since speedup, starting from min(3, time_at_speedup)
            elapsed_since_speedup = (pygame.time.get_ticks() - self.speedup_time) / 1000
            speedup_start = min(3.0, self.time_at_speedup)
            return max(0, speedup_start - elapsed_since_speedup)
        else:
            elapsed = (pygame.time.get_ticks() - self.countdown_start) / 1000
            return max(0, self.countdown_duration - elapsed)
    
    def all_players_chosen(self, players: List[Player]) -> bool:
        """Check if all active players have made their choice."""
        for player in players:
            if player.joined and player.alive and player.choice == Choice.NONE:
                return False
        return True
    
    def trigger_speedup(self):
        """Speed up the countdown to 3 seconds max."""
        if not self.speedup_triggered:
            self.speedup_triggered = True
            self.speedup_time = pygame.time.get_ticks()
            # Calculate current remaining time
            elapsed = (pygame.time.get_ticks() - self.countdown_start) / 1000
            self.time_at_speedup = max(0, self.countdown_duration - elapsed)
    
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
        # Check if all players have chosen - trigger speedup
        if not self.speedup_triggered and self.all_players_chosen(players):
            remaining = self.get_remaining_time()
            if remaining > 3:
                self.trigger_speedup()
        
        if self.get_remaining_time() <= 0:
            # Time's up - go to resolution
            return SceneType.RESOLUTION
        return None
    
    def get_timer_color(self, remaining: float) -> tuple:
        """Get timer color based on remaining time - more red as it gets urgent."""
        if remaining > 5:
            return COLORS['gold']
        elif remaining > 3:
            # Transition from gold to orange
            t = (5 - remaining) / 2
            return (
                255,
                int(215 * (1 - t) + 165 * t),
                int(0 * t)
            )
        else:
            # Transition from orange to red, with pulsing
            t = (3 - remaining) / 3
            pulse = (math.sin(pygame.time.get_ticks() / 100) + 1) / 2
            red_intensity = 200 + int(55 * pulse)
            return (
                red_intensity,
                int(165 * (1 - t)),
                0
            )
    
    def get_timer_scale(self, remaining: float) -> float:
        """Get timer scale factor - bigger as it gets more urgent."""
        if remaining > 5:
            return 1.0
        elif remaining > 3:
            # Grow from 1.0 to 1.3
            t = (5 - remaining) / 2
            return 1.0 + (0.3 * t)
        else:
            # Grow from 1.3 to 2.0 with pulsing
            t = (3 - remaining) / 3
            base_scale = 1.3 + (0.7 * t)
            pulse = (math.sin(pygame.time.get_ticks() / 80) + 1) / 2 * 0.15
            return base_scale + pulse
    
    def get_timer_shake(self, remaining: float) -> tuple:
        """Get shake offset for urgent timer."""
        if remaining > 2:
            return (0, 0)
        
        # Shake intensity increases as time runs out
        intensity = (2 - remaining) / 2 * 8
        shake_x = math.sin(pygame.time.get_ticks() / 30) * intensity
        shake_y = math.cos(pygame.time.get_ticks() / 25) * intensity * 0.5
        return (int(shake_x), int(shake_y))
    
    def draw(self, players: List[Player]):
        """Draw the game scene."""
        self.draw_background()
        
        remaining = self.get_remaining_time()
        
        # Draw player slots first (behind timer)
        for player in players:
            if player.joined:
                draw_player_slot(self.screen, player, show_choice=False, show_controls=True)
        
        if remaining > 0:
            # Get timer styling
            timer_color = self.get_timer_color(remaining)
            timer_scale = self.get_timer_scale(remaining)
            shake_x, shake_y = self.get_timer_shake(remaining)
            
            # Countdown number - render at base size then scale
            countdown_num = int(remaining) + 1
            
            # Use different font sizes based on scale for better quality
            if timer_scale > 1.5:
                base_font = pygame.font.Font(None, 200)
            elif timer_scale > 1.2:
                base_font = pygame.font.Font(None, 160)
            else:
                base_font = constants.FONT_LARGE
            
            countdown_text = base_font.render(str(countdown_num), True, timer_color)
            
            # Scale if needed
            if timer_scale != 1.0 and base_font == constants.FONT_LARGE:
                new_size = (int(countdown_text.get_width() * timer_scale),
                           int(countdown_text.get_height() * timer_scale))
                countdown_text = pygame.transform.smoothscale(countdown_text, new_size)
            
            # Add glow effect for urgency
            if remaining <= 3:
                glow_surf = pygame.Surface((countdown_text.get_width() + 40, 
                                           countdown_text.get_height() + 40), pygame.SRCALPHA)
                glow_color = (*timer_color[:3], 80)
                pygame.draw.ellipse(glow_surf, glow_color, glow_surf.get_rect())
                glow_rect = glow_surf.get_rect(center=(SCREEN_WIDTH // 2 + shake_x, 
                                                       SCREEN_HEIGHT // 2 - 50 + shake_y))
                self.screen.blit(glow_surf, glow_rect)
            
            # Draw shadow for better visibility
            shadow_text = base_font.render(str(countdown_num), True, (0, 0, 0))
            if timer_scale != 1.0 and base_font == constants.FONT_LARGE:
                shadow_text = pygame.transform.smoothscale(shadow_text, new_size)
            shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 4 + shake_x, 
                                                       SCREEN_HEIGHT // 2 - 46 + shake_y))
            self.screen.blit(shadow_text, shadow_rect)
            
            # Draw main timer
            countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2 + shake_x, 
                                                             SCREEN_HEIGHT // 2 - 50 + shake_y))
            self.screen.blit(countdown_text, countdown_rect)
            
            # Instructions - also react to urgency
            if remaining > 3:
                inst_text = "CHOOSE YOUR WEAPON!"
                inst_color = COLORS['white']
            elif remaining > 1:
                inst_text = "HURRY UP!"
                inst_color = COLORS['orange']
            else:
                inst_text = "TIME'S ALMOST UP!"
                inst_color = COLORS['red']
            
            choose_text = constants.FONT_MEDIUM.render(inst_text, True, inst_color)
            choose_rect = choose_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(choose_text, choose_rect)
        
        # Round indicator
        round_text = constants.FONT_SMALL.render(f"Round {self.round_number}", True, COLORS['silver'])
        round_rect = round_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(round_text, round_rect)
        
        # Show "All players ready!" message when everyone has chosen
        if self.all_players_chosen(players) and remaining > 0:
            ready_text = constants.FONT_SMALL.render("All players ready!", True, COLORS['green'])
            ready_rect = ready_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130))
            self.screen.blit(ready_text, ready_rect)

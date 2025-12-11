"""
Resolution scene for Rock Paper Scissors Arena.
"""

import pygame
import math
import random
from typing import List, Optional, Tuple

from scenes.base import Scene
import constants
from constants import SceneType, COLORS, Choice, SCREEN_WIDTH, SCREEN_HEIGHT
from graphics import draw_player_slot, draw_choice_icon
from player import Player, get_alive_count


class ResolutionScene(Scene):
    """Resolution scene showing round results with battle animation."""
    
    def __init__(self, screen: pygame.Surface, bg_surface: pygame.Surface):
        super().__init__(screen, bg_surface)
        self.eliminated_this_round: List[Player] = []
        self.winners: List[Player] = []
        self.losers: List[Player] = []
        self.battle_pairs: List[Tuple[Player, Player]] = []  # (winner, loser) pairs
        self.animation_start = 0
        self.animation_duration = 2.5  # seconds
        self.winning_choice: Optional[Choice] = None
        self.losing_choice: Optional[Choice] = None
        self.particles: List[dict] = []
        self.impact_triggered: List[int] = []  # Track which pairs have triggered impact
    
    def set_eliminated(self, eliminated: List[Player]):
        """Set the list of eliminated players for display."""
        self.eliminated_this_round = eliminated
        self.animation_start = pygame.time.get_ticks()
        self.particles = []
        self.impact_triggered = []
    
    def set_battle_choices(self, winning: Choice, losing: Choice):
        """Set the winning and losing choices for the animation."""
        self.winning_choice = winning
        self.losing_choice = losing
    
    def set_battle_players(self, players: List[Player]):
        """Determine winners and losers and pair them up for animation."""
        self.winners = []
        self.losers = []
        self.battle_pairs = []
        
        if not self.winning_choice or not self.losing_choice:
            return
        
        # Find all winners and losers
        for p in players:
            if p.joined and p.choice != Choice.NONE:
                if p.choice == self.winning_choice:
                    self.winners.append(p)
                elif p.choice == self.losing_choice:
                    self.losers.append(p)
        
        # Pair up winners with losers (each winner attacks a loser)
        if self.winners and self.losers:
            for i, winner in enumerate(self.winners):
                # Each winner targets a loser (cycle through if more winners than losers)
                loser = self.losers[i % len(self.losers)]
                self.battle_pairs.append((winner, loser))
    
    def get_animation_progress(self) -> float:
        """Get animation progress from 0.0 to 1.0."""
        elapsed = (pygame.time.get_ticks() - self.animation_start) / 1000
        return min(1.0, elapsed / self.animation_duration)
    
    def is_animation_complete(self) -> bool:
        """Check if the animation has finished."""
        return self.get_animation_progress() >= 1.0
    
    def spawn_impact_particles(self, x: int, y: int, color: Tuple[int, int, int]):
        """Spawn particles at impact point."""
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(150, 400)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 1.0,
                'color': color,
                'size': random.randint(5, 15)
            })
    
    def update_particles(self, dt: float):
        """Update particle positions and lifetimes."""
        for p in self.particles:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['vy'] += 500 * dt  # gravity
            p['life'] -= dt * 1.2
        self.particles = [p for p in self.particles if p['life'] > 0]
    
    def draw_particles(self):
        """Draw all active particles."""
        for p in self.particles:
            alpha = int(255 * p['life'])
            color = (*p['color'][:3], alpha)
            size = int(p['size'] * p['life'])
            if size > 0:
                surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, color, (size, size), size)
                self.screen.blit(surf, (int(p['x'] - size), int(p['y'] - size)))
    
    def get_battle_verb(self) -> str:
        """Get the action verb for the winning choice."""
        if self.winning_choice == Choice.ROCK:
            return "CRUSHES"
        elif self.winning_choice == Choice.SCISSORS:
            return "CUTS"
        elif self.winning_choice == Choice.PAPER:
            return "COVERS"
        return "BEATS"
    
    def handle_event(self, event: pygame.event.Event, players: List[Player]) -> Optional[SceneType]:
        """Handle resolution input events."""
        if event.type != pygame.KEYDOWN:
            return None
        
        # Only allow continuing after animation is complete
        if event.key == pygame.K_SPACE and self.is_animation_complete():
            alive_count = get_alive_count(players)
            if alive_count <= 1:
                return SceneType.VICTORY
            else:
                return SceneType.GAME
        
        return None
    
    def update(self, players: List[Player]) -> Optional[SceneType]:
        """Update resolution state."""
        dt = 1 / 60  # Assume 60 FPS
        self.update_particles(dt)
        
        # Check for impact moments and spawn particles
        progress = self.get_animation_progress()
        impact_time = 0.5  # When impact happens
        
        if progress >= impact_time:
            for i, (winner, loser) in enumerate(self.battle_pairs):
                if i not in self.impact_triggered:
                    self.impact_triggered.append(i)
                    # Spawn particles at loser's position
                    self.spawn_impact_particles(
                        loser.position[0],
                        loser.position[1],
                        loser.color
                    )
        
        return None
    
    def draw_battle_animation(self, players: List[Player]):
        """Draw the battle animation with icons traveling between players."""
        progress = self.get_animation_progress()
        
        # Animation phases:
        # 0.0-0.5: Winner icons travel from their position to loser positions
        # 0.5-1.0: Impact and defeat animation at loser positions
        
        for i, (winner, loser) in enumerate(self.battle_pairs):
            winner_pos = winner.position
            loser_pos = loser.position
            
            if progress < 0.5:
                # Travel phase - winner icon moves toward loser
                travel_progress = progress / 0.5
                # Ease in-out
                ease = travel_progress * travel_progress * (3 - 2 * travel_progress)
                
                # Calculate current position (interpolate from winner to loser)
                current_x = winner_pos[0] + (loser_pos[0] - winner_pos[0]) * ease
                current_y = winner_pos[1] + (loser_pos[1] - winner_pos[1]) * ease
                
                # Add a slight arc to the movement
                arc_height = -100 * math.sin(travel_progress * math.pi)
                current_y += arc_height
                
                # Size grows slightly as it approaches
                size = 45 + int(15 * ease)
                
                # Draw the traveling winner icon
                draw_choice_icon(self.screen, winner.choice, int(current_x), int(current_y), 
                               size, winner.color, 0)
                
                # Draw a trail effect
                for t in range(3):
                    trail_progress = max(0, travel_progress - (t + 1) * 0.08)
                    if trail_progress > 0:
                        trail_ease = trail_progress * trail_progress * (3 - 2 * trail_progress)
                        trail_x = winner_pos[0] + (loser_pos[0] - winner_pos[0]) * trail_ease
                        trail_y = winner_pos[1] + (loser_pos[1] - winner_pos[1]) * trail_ease
                        trail_y += -100 * math.sin(trail_progress * math.pi)
                        trail_size = int((45 + 15 * trail_ease) * (0.7 - t * 0.2))
                        trail_color = tuple(max(50, c - 40 * (t + 1)) for c in winner.color)
                        if trail_size > 10:
                            draw_choice_icon(self.screen, winner.choice, int(trail_x), int(trail_y),
                                           trail_size, trail_color, 0)
            
            else:
                # Impact phase - winner bounces at loser position, loser is defeated
                impact_progress = (progress - 0.5) / 0.5
                
                # Winner bounces/pulses at the loser's position
                bounce = math.sin(impact_progress * math.pi * 3) * 15 * (1 - impact_progress)
                winner_size = 60 + int(bounce)
                
                # Draw victorious winner icon at loser's position
                draw_choice_icon(self.screen, winner.choice, loser_pos[0], loser_pos[1],
                               winner_size, winner.color, 0)
        
        # Draw particles
        self.draw_particles()
        
        # Show battle result text in center after impact
        if progress > 0.5 and self.winning_choice and self.losing_choice:
            text_alpha = min(255, int((progress - 0.5) * 2 * 255))
            
            verb = self.get_battle_verb()
            winner_name = self.winning_choice.name
            loser_name = self.losing_choice.name
            
            # Create text with shadow for better visibility
            result_text = constants.FONT_MEDIUM.render(f"{winner_name} {verb} {loser_name}!", True, COLORS['gold'])
            shadow_text = constants.FONT_MEDIUM.render(f"{winner_name} {verb} {loser_name}!", True, (0, 0, 0))
            
            result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 + 3))
            
            shadow_text.set_alpha(text_alpha)
            result_text.set_alpha(text_alpha)
            
            self.screen.blit(shadow_text, shadow_rect)
            self.screen.blit(result_text, result_rect)
    
    def draw(self, players: List[Player]):
        """Draw the resolution scene."""
        self.draw_background()
        
        progress = self.get_animation_progress()
        
        # Draw all player slots with choices revealed
        # But hide the choice icon for losers after impact (it's been "defeated")
        for player in players:
            if player.joined:
                # During animation, don't show loser's choice after impact
                show_choice = True
                if progress > 0.5 and player in self.losers:
                    show_choice = False  # Choice has been defeated
                
                # For winners during travel phase, dim their slot choice 
                # (since it's traveling)
                if progress < 0.5 and player in self.winners:
                    show_choice = False  # It's traveling
                
                draw_player_slot(self.screen, player, show_choice=show_choice, show_controls=False)
        
        # Draw battle animation if there was a winner/loser
        if self.battle_pairs:
            self.draw_battle_animation(players)
        elif not self.winning_choice:
            # Draw "DRAW" text for ties
            if progress > 0.3:
                # Shadow
                shadow = constants.FONT_LARGE.render("DRAW!", True, (0, 0, 0))
                shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + 4, SCREEN_HEIGHT // 2 - 46))
                self.screen.blit(shadow, shadow_rect)
                
                draw_text = constants.FONT_LARGE.render("DRAW!", True, COLORS['cyan'])
                draw_rect = draw_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
                self.screen.blit(draw_text, draw_rect)
                
                no_elim = constants.FONT_MEDIUM.render("No eliminations", True, COLORS['silver'])
                no_elim_rect = no_elim.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
                self.screen.blit(no_elim, no_elim_rect)
        
        # Show elimination status after animation
        if self.is_animation_complete():
            if self.eliminated_this_round:
                elim_names = ", ".join([f"P{p.id}" for p in self.eliminated_this_round])
                elim_text = constants.FONT_SMALL.render(f"Eliminated: {elim_names}", True, COLORS['red'])
                elim_rect = elim_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
                self.screen.blit(elim_text, elim_rect)
            
            # Continue prompt
            alive = get_alive_count(players)
            if alive <= 1:
                cont_text = "Press SPACE to see the winner!"
            else:
                cont_text = f"Press SPACE to continue ({alive} players remaining)"
            cont = constants.FONT_SMALL.render(cont_text, True, COLORS['green'])
            cont_rect = cont.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(cont, cont_rect)

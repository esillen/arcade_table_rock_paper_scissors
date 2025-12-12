"""
Rock Paper Scissors - Local Multiplayer Arena
Main game class managing scenes and game state.
"""

import pygame

from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from core.enums import SceneType
from core.player import create_players
from core.rules import resolve_round, get_round_choices, get_choosers, get_non_choosers
from graphics.fonts import init_fonts
from graphics.background import create_background_surface
from scenes import MenuScene, GameScene, ResolutionScene, VictoryScene


class Game:
    """Main game class managing scenes and game state."""
    
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.font.init()
        init_fonts()
        
        # Screen setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Rock Paper Scissors Arena")
        
        # Game state
        self.players = create_players()
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Pre-render background
        self.bg_surface = create_background_surface()
        
        # Initialize scenes
        self.scenes = {
            SceneType.MENU: MenuScene(self.screen, self.bg_surface),
            SceneType.GAME: GameScene(self.screen, self.bg_surface),
            SceneType.RESOLUTION: ResolutionScene(self.screen, self.bg_surface),
            SceneType.VICTORY: VictoryScene(self.screen, self.bg_surface),
        }
        self.current_scene_type = SceneType.MENU
    
    @property
    def current_scene(self):
        """Get the current scene instance."""
        return self.scenes[self.current_scene_type]
    
    def change_scene(self, new_scene: SceneType):
        """Handle scene transitions with appropriate setup."""
        old_scene = self.current_scene_type
        self.current_scene_type = new_scene
        
        if new_scene == SceneType.MENU:
            # Reset all players for a new game
            for player in self.players:
                player.reset_for_new_game()
            self.scenes[SceneType.GAME].reset_game()
        
        elif new_scene == SceneType.GAME:
            # Reset choices and start countdown
            for player in self.players:
                player.reset_choice()
            
            if old_scene == SceneType.MENU:
                self.scenes[SceneType.GAME].reset_game()
            else:
                self.scenes[SceneType.GAME].reset_round()
            
            self.scenes[SceneType.GAME].start_countdown()
        
        elif new_scene == SceneType.RESOLUTION:
            # Get the winning/losing choices before resolving (for animation)
            winning_choice, losing_choice, is_majority, is_no_choice = get_round_choices(self.players)
            
            # Set up battle animation BEFORE resolving (need player states)
            if is_no_choice:
                # Special case: players who didn't choose get eliminated
                choosers = get_choosers(self.players)
                non_choosers = get_non_choosers(self.players)
                self.scenes[SceneType.RESOLUTION].set_no_choice_battle(choosers, non_choosers)
            else:
                self.scenes[SceneType.RESOLUTION].set_battle_choices(winning_choice, losing_choice, is_majority)
                self.scenes[SceneType.RESOLUTION].set_battle_players(self.players)
            
            # Resolve the round and set eliminated players
            eliminated = resolve_round(self.players)
            self.scenes[SceneType.RESOLUTION].set_eliminated(eliminated)
        
        elif new_scene == SceneType.VICTORY:
            # Set the winner
            self.scenes[SceneType.VICTORY].set_winner(self.players)
    
    def handle_events(self):
        """Handle all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
                return
            
            # Let current scene handle the event
            new_scene = self.current_scene.handle_event(event, self.players)
            if new_scene:
                self.change_scene(new_scene)
    
    def update(self):
        """Update game state."""
        new_scene = self.current_scene.update(self.players)
        if new_scene:
            self.change_scene(new_scene)
    
    def draw(self):
        """Draw current scene."""
        self.current_scene.draw(self.players)
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

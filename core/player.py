"""
Player class for Rock Paper Scissors Arena.
"""

from dataclasses import dataclass
from typing import List, Tuple

from core.enums import Choice
from config.colors import PLAYER_COLORS
from config.controls import PLAYER_CONFIGS, PLAYER_POSITIONS


@dataclass
class Player:
    """Represents a player in the game."""
    id: int
    color: Tuple[int, int, int]
    join_key: int
    rock_key: int
    paper_key: int
    scissors_key: int
    position: Tuple[int, int] = (0, 0)
    angle: float = 0.0
    joined: bool = False
    alive: bool = True
    choice: Choice = Choice.NONE
    
    def reset_choice(self):
        """Reset player's choice for a new round."""
        self.choice = Choice.NONE
    
    def reset_for_new_game(self):
        """Reset player state for a new game."""
        self.joined = False
        self.alive = True
        self.choice = Choice.NONE
    
    def eliminate(self):
        """Eliminate the player from the current game."""
        self.alive = False
    
    def make_choice(self, choice: Choice):
        """Make a choice if player hasn't chosen yet."""
        if self.choice == Choice.NONE:
            self.choice = choice
    
    def handle_input(self, key: int) -> bool:
        """
        Handle a key press for this player.
        Returns True if the key was handled.
        """
        if not self.joined or not self.alive:
            return False
        
        if self.choice != Choice.NONE:
            return False
        
        if key == self.rock_key:
            self.choice = Choice.ROCK
            return True
        elif key == self.paper_key:
            self.choice = Choice.PAPER
            return True
        elif key == self.scissors_key:
            self.choice = Choice.SCISSORS
            return True
        
        return False


def create_players() -> List[Player]:
    """Create all 8 players with their configurations."""
    players = []
    for i, (config, pos) in enumerate(zip(PLAYER_CONFIGS, PLAYER_POSITIONS)):
        player = Player(
            id=i + 1,
            color=PLAYER_COLORS[i],
            join_key=config[0],
            rock_key=config[1],
            paper_key=config[2],
            scissors_key=config[3],
            position=(pos[0], pos[1]),
            angle=pos[2]
        )
        players.append(player)
    return players


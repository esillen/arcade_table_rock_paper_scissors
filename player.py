"""
Player class and related logic for Rock Paper Scissors Arena.
"""

import pygame
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

from constants import Choice, PLAYER_COLORS


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


# Player configurations - positioned around the screen
# Keys: (join_key, rock_key, paper_key, scissors_key)
PLAYER_CONFIGS = [
    # Top row (facing down)
    (pygame.K_1, pygame.K_q, pygame.K_w, pygame.K_e),      # Player 1 - top left
    (pygame.K_2, pygame.K_r, pygame.K_t, pygame.K_y),      # Player 2 - top center-left
    (pygame.K_3, pygame.K_u, pygame.K_i, pygame.K_o),      # Player 3 - top center-right
    (pygame.K_4, pygame.K_p, pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET),  # Player 4 - top right
    # Bottom row (facing up)
    (pygame.K_5, pygame.K_z, pygame.K_x, pygame.K_c),      # Player 5 - bottom left
    (pygame.K_6, pygame.K_v, pygame.K_b, pygame.K_n),      # Player 6 - bottom center-left
    (pygame.K_7, pygame.K_m, pygame.K_COMMA, pygame.K_PERIOD),  # Player 7 - bottom center-right
    (pygame.K_8, pygame.K_SEMICOLON, pygame.K_QUOTE, pygame.K_RETURN),  # Player 8 - bottom right
]

# Positions around the screen (x, y, angle) - anti-clockwise from bottom center
# Screen is laying flat on table, players stand around it
PLAYER_POSITIONS = [
    (640, 820, 0),      # P1: Bottom center - facing up
    (1100, 750, 45),    # P2: Bottom right corner - facing diagonally
    (1200, 450, 90),    # P3: Right center - facing left
    (1100, 150, 135),   # P4: Top right corner - facing diagonally
    (640, 80, 180),     # P5: Top center - facing down
    (180, 150, 225),    # P6: Top left corner - facing diagonally
    (80, 450, 270),     # P7: Left center - facing right
    (180, 750, 315),    # P8: Bottom left corner - facing diagonally
]


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


def get_choice_counts(players: List[Player]) -> dict:
    """Count how many players chose each option."""
    counts = {Choice.ROCK: 0, Choice.PAPER: 0, Choice.SCISSORS: 0}
    for p in players:
        if p.joined and p.alive and p.choice != Choice.NONE:
            counts[p.choice] += 1
    return counts


def get_what_beats(choice: Choice) -> Choice:
    """Get what the given choice beats."""
    if choice == Choice.ROCK:
        return Choice.SCISSORS
    elif choice == Choice.SCISSORS:
        return Choice.PAPER
    elif choice == Choice.PAPER:
        return Choice.ROCK
    return None


def resolve_round(players: List[Player]) -> List[Player]:
    """
    Resolve a round of rock paper scissors.
    Returns list of players who are eliminated this round.
    
    Rules:
    - If all players chose the same: no elimination
    - If all three choices are present:
      - If there's a majority, that majority defeats what it beats
      - If no majority (all equal), it's a draw
    - If only two choices present: standard RPS rules apply, losers eliminated
    """
    active_players = [p for p in players if p.joined and p.alive and p.choice != Choice.NONE]
    
    if len(active_players) < 2:
        return []
    
    # Count choices
    counts = get_choice_counts(players)
    present_choices = [c for c in counts if counts[c] > 0]
    
    # All same = draw
    if len(present_choices) == 1:
        return []
    
    losing_choice = None
    
    if len(present_choices) == 3:
        # All three choices present - check for majority
        max_count = max(counts.values())
        majority_choices = [c for c in counts if counts[c] == max_count]
        
        if len(majority_choices) == 1:
            # There's a clear majority - they defeat what they beat
            majority = majority_choices[0]
            losing_choice = get_what_beats(majority)
        else:
            # No clear majority (tie between 2+ choices) = draw
            return []
    else:
        # Two choices - standard RPS rules
        c1, c2 = present_choices[0], present_choices[1]
        
        # Determine losing choice
        # Rock beats Scissors, Scissors beats Paper, Paper beats Rock
        if (c1 == Choice.ROCK and c2 == Choice.SCISSORS) or (c1 == Choice.SCISSORS and c2 == Choice.ROCK):
            losing_choice = Choice.SCISSORS
        elif (c1 == Choice.SCISSORS and c2 == Choice.PAPER) or (c1 == Choice.PAPER and c2 == Choice.SCISSORS):
            losing_choice = Choice.PAPER
        elif (c1 == Choice.PAPER and c2 == Choice.ROCK) or (c1 == Choice.ROCK and c2 == Choice.PAPER):
            losing_choice = Choice.ROCK
    
    # Eliminate players with losing choice
    eliminated = []
    if losing_choice:
        for player in active_players:
            if player.choice == losing_choice:
                player.eliminate()
                eliminated.append(player)
    
    return eliminated


def get_joined_count(players: List[Player]) -> int:
    """Get the number of players who have joined."""
    return sum(1 for p in players if p.joined)


def get_alive_count(players: List[Player]) -> int:
    """Get the number of players still alive."""
    return sum(1 for p in players if p.joined and p.alive)


def get_winner(players: List[Player]) -> Player:
    """Get the winning player (if only one alive)."""
    for player in players:
        if player.joined and player.alive:
            return player
    return None


def get_round_choices(players: List[Player]) -> Tuple[Optional[Choice], Optional[Choice], bool]:
    """
    Get the winning and losing choices from the round.
    Returns (winning_choice, losing_choice, is_majority_rule) or (None, None, False) if draw.
    
    is_majority_rule is True when all three choices were present but majority won.
    """
    # Count choices for active players (before elimination)
    counts = {Choice.ROCK: 0, Choice.PAPER: 0, Choice.SCISSORS: 0}
    for p in players:
        if p.joined and p.choice != Choice.NONE:
            # Count if player is alive OR was just eliminated this round
            # (we call this before resolve_round, so all are still "alive")
            counts[p.choice] += 1
    
    present_choices = [c for c in counts if counts[c] > 0]
    
    # All same = draw
    if len(present_choices) == 1:
        return (None, None, False)
    
    if len(present_choices) == 3:
        # All three choices present - check for majority
        max_count = max(counts.values())
        majority_choices = [c for c in counts if counts[c] == max_count]
        
        if len(majority_choices) == 1:
            # There's a clear majority - they defeat what they beat
            majority = majority_choices[0]
            losing = get_what_beats(majority)
            return (majority, losing, True)  # True = majority rule
        else:
            # No clear majority = draw
            return (None, None, False)
    
    # Two choices - standard RPS rules
    c1, c2 = present_choices[0], present_choices[1]
    
    # Determine winning and losing choice
    if (c1 == Choice.ROCK and c2 == Choice.SCISSORS) or (c1 == Choice.SCISSORS and c2 == Choice.ROCK):
        return (Choice.ROCK, Choice.SCISSORS, False)
    elif (c1 == Choice.SCISSORS and c2 == Choice.PAPER) or (c1 == Choice.PAPER and c2 == Choice.SCISSORS):
        return (Choice.SCISSORS, Choice.PAPER, False)
    elif (c1 == Choice.PAPER and c2 == Choice.ROCK) or (c1 == Choice.ROCK and c2 == Choice.PAPER):
        return (Choice.PAPER, Choice.ROCK, False)
    
    return (None, None, False)


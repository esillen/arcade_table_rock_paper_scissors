"""
Game rules and resolution logic for Rock Paper Scissors Arena.
"""

from typing import List, Tuple, Optional

from core.enums import Choice
from core.player import Player


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
    - Players who didn't choose are eliminated first (if anyone else chose)
    - If all players chose the same: no elimination
    - If all three choices are present:
      - If there's a majority, that majority defeats what it beats
      - If no majority (all equal), it's a draw
    - If only two choices present: standard RPS rules apply, losers eliminated
    """
    all_alive = [p for p in players if p.joined and p.alive]
    players_who_chose = [p for p in all_alive if p.choice != Choice.NONE]
    players_who_didnt = [p for p in all_alive if p.choice == Choice.NONE]
    
    # First: eliminate anyone who didn't choose (if at least one person did choose)
    if players_who_didnt and players_who_chose:
        eliminated = []
        for player in players_who_didnt:
            player.eliminate()
            eliminated.append(player)
        return eliminated  # Only eliminate non-choosers this round
    
    # If no one chose or only one person chose, no elimination
    if len(players_who_chose) < 2:
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
        for player in players_who_chose:
            if player.choice == losing_choice:
                player.eliminate()
                eliminated.append(player)
    
    return eliminated


def get_non_choosers(players: List[Player]) -> List[Player]:
    """Get list of alive players who didn't make a choice."""
    return [p for p in players if p.joined and p.alive and p.choice == Choice.NONE]


def get_choosers(players: List[Player]) -> List[Player]:
    """Get list of alive players who made a choice."""
    return [p for p in players if p.joined and p.alive and p.choice != Choice.NONE]


def get_round_choices(players: List[Player]) -> Tuple[Optional[Choice], Optional[Choice], bool, bool]:
    """
    Get the winning and losing choices from the round.
    Returns (winning_choice, losing_choice, is_majority_rule, is_no_choice) 
    or (None, None, False, False) if draw.
    
    is_majority_rule is True when all three choices were present but majority won.
    is_no_choice is True when some players didn't choose (they get eliminated).
    """
    # Check for non-choosers first
    non_choosers = get_non_choosers(players)
    choosers = get_choosers(players)
    
    if non_choosers and choosers:
        # Some players didn't choose - they get eliminated
        # Return special case: no winning/losing choice, but is_no_choice=True
        return (None, None, False, True)
    
    # Count choices for active players (before elimination)
    counts = {Choice.ROCK: 0, Choice.PAPER: 0, Choice.SCISSORS: 0}
    for p in players:
        if p.joined and p.choice != Choice.NONE:
            counts[p.choice] += 1
    
    present_choices = [c for c in counts if counts[c] > 0]
    
    # All same = draw
    if len(present_choices) <= 1:
        return (None, None, False, False)
    
    if len(present_choices) == 3:
        # All three choices present - check for majority
        max_count = max(counts.values())
        majority_choices = [c for c in counts if counts[c] == max_count]
        
        if len(majority_choices) == 1:
            # There's a clear majority - they defeat what they beat
            majority = majority_choices[0]
            losing = get_what_beats(majority)
            return (majority, losing, True, False)  # True = majority rule
        else:
            # No clear majority = draw
            return (None, None, False, False)
    
    # Two choices - standard RPS rules
    c1, c2 = present_choices[0], present_choices[1]
    
    # Determine winning and losing choice
    if (c1 == Choice.ROCK and c2 == Choice.SCISSORS) or (c1 == Choice.SCISSORS and c2 == Choice.ROCK):
        return (Choice.ROCK, Choice.SCISSORS, False, False)
    elif (c1 == Choice.SCISSORS and c2 == Choice.PAPER) or (c1 == Choice.PAPER and c2 == Choice.SCISSORS):
        return (Choice.SCISSORS, Choice.PAPER, False, False)
    elif (c1 == Choice.PAPER and c2 == Choice.ROCK) or (c1 == Choice.ROCK and c2 == Choice.PAPER):
        return (Choice.PAPER, Choice.ROCK, False, False)
    
    return (None, None, False, False)


def get_joined_count(players: List[Player]) -> int:
    """Get the number of players who have joined."""
    return sum(1 for p in players if p.joined)


def get_alive_count(players: List[Player]) -> int:
    """Get the number of players still alive."""
    return sum(1 for p in players if p.joined and p.alive)


def get_winner(players: List[Player]) -> Optional[Player]:
    """Get the winning player (if only one alive)."""
    for player in players:
        if player.joined and player.alive:
            return player
    return None


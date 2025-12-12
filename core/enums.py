"""
Enumerations for Rock Paper Scissors Arena.
"""

from enum import Enum


class Choice(Enum):
    """Player choice in rock paper scissors."""
    NONE = 0
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class SceneType(Enum):
    """Game scene types."""
    MENU = 1
    GAME = 2
    RESOLUTION = 3
    VICTORY = 4


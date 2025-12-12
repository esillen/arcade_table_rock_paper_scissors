#!/usr/bin/env python3
"""
Rock Paper Scissors Arena - Entry Point

A local multiplayer game for up to 8 players standing around the screen.
"""

from game import Game


def main():
    """Start the game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()


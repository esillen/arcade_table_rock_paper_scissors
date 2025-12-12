"""
Player control configurations and table positions.
"""

import pygame

# Player key configurations
# Format: (join_key, rock_key, paper_key, scissors_key)
PLAYER_CONFIGS = [
    (pygame.K_1, pygame.K_q, pygame.K_w, pygame.K_e),      # Player 1
    (pygame.K_2, pygame.K_r, pygame.K_t, pygame.K_y),      # Player 2
    (pygame.K_3, pygame.K_u, pygame.K_i, pygame.K_o),      # Player 3
    (pygame.K_4, pygame.K_p, pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET),  # Player 4
    (pygame.K_5, pygame.K_z, pygame.K_x, pygame.K_c),      # Player 5
    (pygame.K_6, pygame.K_v, pygame.K_b, pygame.K_n),      # Player 6
    (pygame.K_7, pygame.K_m, pygame.K_COMMA, pygame.K_PERIOD),  # Player 7
    (pygame.K_8, pygame.K_SEMICOLON, pygame.K_QUOTE, pygame.K_RETURN),  # Player 8
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


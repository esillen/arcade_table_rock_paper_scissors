"""
Player slot UI rendering for Rock Paper Scissors Arena.
"""

import pygame

from config.colors import COLORS
from core.enums import Choice
from graphics.fonts import font_medium, font_small, font_tiny
from graphics.icons import draw_rock, draw_paper, draw_scissors, draw_choice_icon


def draw_player_slot(surface: pygame.Surface, player, show_choice: bool = False,
                     show_controls: bool = True):
    """
    Draw a player's slot on screen, rotated to face the player.
    The entire slot is rendered to a temp surface then rotated.
    """
    x, y = player.position
    angle = player.angle
    
    # Slot dimensions
    slot_width, slot_height = 200, 160
    
    # Create a temporary surface for the entire slot (rendered upright, then rotated)
    temp_surface = pygame.Surface((slot_width, slot_height), pygame.SRCALPHA)
    cx, cy = slot_width // 2, slot_height // 2  # Center of temp surface
    
    is_eliminated = player.joined and not player.alive
    
    # Draw slot background with player color tint
    if is_eliminated:
        # Darker, damaged-looking background for eliminated players
        bg_color = (30, 15, 15, 200)
    else:
        bg_color = tuple(c // 6 for c in player.color) + (180,)
    pygame.draw.rect(temp_surface, bg_color, (0, 0, slot_width, slot_height), border_radius=15)
    
    # For eliminated players, add crack lines to show damage
    if is_eliminated:
        crack_color = (60, 30, 30)
        # Draw crack patterns
        pygame.draw.line(temp_surface, crack_color, (20, 30), (80, 70), 2)
        pygame.draw.line(temp_surface, crack_color, (80, 70), (60, 120), 2)
        pygame.draw.line(temp_surface, crack_color, (80, 70), (120, 90), 2)
        pygame.draw.line(temp_surface, crack_color, (180, 40), (140, 80), 2)
        pygame.draw.line(temp_surface, crack_color, (140, 80), (160, 130), 2)
        pygame.draw.line(temp_surface, crack_color, (140, 80), (100, 110), 2)
        pygame.draw.line(temp_surface, crack_color, (30, 140), (70, 100), 2)
        pygame.draw.line(temp_surface, crack_color, (170, 140), (130, 110), 2)
    
    # Border color based on state
    if not player.joined:
        border_color = (80, 80, 80)
    elif is_eliminated:
        border_color = (100, 40, 40)
    else:
        border_color = player.color
    
    pygame.draw.rect(temp_surface, border_color, (0, 0, slot_width, slot_height), 4, border_radius=15)
    
    # Player number (near top of slot) - dimmed for eliminated
    if is_eliminated:
        num_color = (100, 50, 50)
    elif player.joined:
        num_color = player.color
    else:
        num_color = (100, 100, 100)
    num_text = font_medium().render(f"P{player.id}", True, num_color)
    num_rect = num_text.get_rect(center=(cx, 35))
    temp_surface.blit(num_text, num_rect)
    
    if not player.joined:
        # Show join prompt with ready key (rock/left key)
        ready_key_name = pygame.key.name(player.rock_key).upper()
        join_text = font_small().render(f"Press {ready_key_name}", True, (150, 150, 150))
        join_rect = join_text.get_rect(center=(cx, 80))
        temp_surface.blit(join_text, join_rect)
    elif is_eliminated:
        # Show eliminated text
        elim_text = font_small().render("ELIMINATED", True, (200, 60, 60))
        elim_rect = elim_text.get_rect(center=(cx, 100))
        temp_surface.blit(elim_text, elim_rect)
        
        # Draw big red X over the slot
        x_color = (220, 50, 50)
        x_thickness = 8
        padding = 25
        # Top-left to bottom-right
        pygame.draw.line(temp_surface, x_color, 
                        (padding, padding), 
                        (slot_width - padding, slot_height - padding), 
                        x_thickness)
        # Top-right to bottom-left
        pygame.draw.line(temp_surface, x_color, 
                        (slot_width - padding, padding), 
                        (padding, slot_height - padding), 
                        x_thickness)
        
        # Draw darker outline for the X for better visibility
        x_outline = (120, 20, 20)
        pygame.draw.line(temp_surface, x_outline, 
                        (padding, padding), 
                        (slot_width - padding, slot_height - padding), 
                        x_thickness + 4)
        pygame.draw.line(temp_surface, x_outline, 
                        (slot_width - padding, padding), 
                        (padding, slot_height - padding), 
                        x_thickness + 4)
        # Redraw red X on top
        pygame.draw.line(temp_surface, x_color, 
                        (padding, padding), 
                        (slot_width - padding, slot_height - padding), 
                        x_thickness)
        pygame.draw.line(temp_surface, x_color, 
                        (slot_width - padding, padding), 
                        (padding, slot_height - padding), 
                        x_thickness)
        
    elif show_choice and player.choice != Choice.NONE:
        # Show their choice icon
        draw_choice_icon(temp_surface, player.choice, cx, 100, 40, player.color, 0)
    elif show_controls:
        # Show control hints
        r_key = pygame.key.name(player.rock_key).upper()
        p_key = pygame.key.name(player.paper_key).upper()
        s_key = pygame.key.name(player.scissors_key).upper()
        
        if player.choice == Choice.NONE:
            hint_text = font_tiny().render(f"{r_key}  {p_key}  {s_key}", True, (180, 180, 180))
        else:
            hint_text = font_tiny().render("LOCKED IN!", True, COLORS['green'])
        
        hint_rect = hint_text.get_rect(center=(cx, 75))
        temp_surface.blit(hint_text, hint_rect)
        
        # Show mini icons for controls
        spacing = 50
        draw_rock(temp_surface, cx - spacing, 115, 18, (120, 120, 120), 0)
        draw_paper(temp_surface, cx, 115, 18, (120, 120, 120), 0)
        draw_scissors(temp_surface, cx + spacing, 115, 18, (120, 120, 120), 0)
    
    # Rotate the entire slot surface
    rotated_surface = pygame.transform.rotate(temp_surface, angle)
    rotated_rect = rotated_surface.get_rect(center=(x, y))
    surface.blit(rotated_surface, rotated_rect)


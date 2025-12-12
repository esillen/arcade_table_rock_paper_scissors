"""
Vector graphics drawing functions for Rock Paper Scissors Arena.
"""

import pygame
import math
from typing import Tuple

import constants
from constants import Choice, COLORS, SCREEN_WIDTH, SCREEN_HEIGHT


def draw_rock(surface: pygame.Surface, x: int, y: int, size: int, 
              color: Tuple[int, int, int], angle: float = 0):
    """Draw a rock (fist) icon using vector graphics."""
    temp_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
    cx, cy = size, size
    
    fist_color = color
    darker = tuple(max(0, c - 60) for c in color)
    
    # Palm base
    pygame.draw.ellipse(temp_surface, fist_color, 
                       (cx - size * 0.4, cy - size * 0.3, size * 0.8, size * 0.7))
    
    # Knuckle bumps
    knuckle_positions = [
        (cx - size * 0.25, cy - size * 0.35),
        (cx, cy - size * 0.4),
        (cx + size * 0.25, cy - size * 0.35),
    ]
    for kx, ky in knuckle_positions:
        pygame.draw.circle(temp_surface, fist_color, (int(kx), int(ky)), int(size * 0.18))
    
    # Finger fold lines
    pygame.draw.arc(temp_surface, darker,
                   (cx - size * 0.35, cy - size * 0.25, size * 0.25, size * 0.2),
                   0, math.pi, 2)
    pygame.draw.arc(temp_surface, darker,
                   (cx - size * 0.1, cy - size * 0.3, size * 0.25, size * 0.2),
                   0, math.pi, 2)
    pygame.draw.arc(temp_surface, darker,
                   (cx + size * 0.12, cy - size * 0.25, size * 0.25, size * 0.2),
                   0, math.pi, 2)
    
    # Thumb
    thumb_points = [
        (cx - size * 0.4, cy + size * 0.1),
        (cx - size * 0.5, cy - size * 0.1),
        (cx - size * 0.45, cy - size * 0.2),
        (cx - size * 0.35, cy - size * 0.15),
        (cx - size * 0.35, cy + size * 0.1),
    ]
    pygame.draw.polygon(temp_surface, fist_color, thumb_points)
    
    # Outline
    pygame.draw.ellipse(temp_surface, darker, 
                       (cx - size * 0.4, cy - size * 0.3, size * 0.8, size * 0.7), 3)
    
    # Rotate and blit
    if angle != 0:
        temp_surface = pygame.transform.rotate(temp_surface, angle)
    rect = temp_surface.get_rect(center=(x, y))
    surface.blit(temp_surface, rect)


def draw_paper(surface: pygame.Surface, x: int, y: int, size: int,
               color: Tuple[int, int, int], angle: float = 0):
    """Draw a paper (open hand) icon using vector graphics."""
    temp_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
    cx, cy = size, size
    
    paper_color = color
    darker = tuple(max(0, c - 60) for c in color)
    
    # Palm
    palm_rect = (cx - size * 0.3, cy - size * 0.1, size * 0.6, size * 0.5)
    pygame.draw.ellipse(temp_surface, paper_color, palm_rect)
    
    # Fingers
    finger_data = [
        (cx - size * 0.25, -size * 0.45, size * 0.12),  # Index
        (cx - size * 0.08, -size * 0.52, size * 0.12),  # Middle
        (cx + size * 0.1, -size * 0.48, size * 0.12),   # Ring
        (cx + size * 0.26, -size * 0.38, size * 0.11),  # Pinky
    ]
    
    for fx, fy_offset, width in finger_data:
        finger_rect = pygame.Rect(fx - width, cy + fy_offset, width * 2, size * 0.5)
        pygame.draw.ellipse(temp_surface, paper_color, finger_rect)
        pygame.draw.ellipse(temp_surface, darker, finger_rect, 2)
    
    # Thumb
    thumb_points = [
        (cx - size * 0.3, cy + size * 0.15),
        (cx - size * 0.5, cy),
        (cx - size * 0.55, cy - size * 0.15),
        (cx - size * 0.45, cy - size * 0.25),
        (cx - size * 0.35, cy - size * 0.15),
        (cx - size * 0.35, cy + size * 0.1),
    ]
    pygame.draw.polygon(temp_surface, paper_color, thumb_points)
    pygame.draw.polygon(temp_surface, darker, thumb_points, 2)
    
    # Palm outline
    pygame.draw.ellipse(temp_surface, darker, palm_rect, 2)
    
    # Rotate and blit
    if angle != 0:
        temp_surface = pygame.transform.rotate(temp_surface, angle)
    rect = temp_surface.get_rect(center=(x, y))
    surface.blit(temp_surface, rect)


def draw_scissors(surface: pygame.Surface, x: int, y: int, size: int,
                  color: Tuple[int, int, int], angle: float = 0):
    """Draw scissors icon using vector graphics."""
    temp_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
    cx, cy = size, size
    
    scissors_color = color
    darker = tuple(max(0, c - 60) for c in color)
    metal = (200, 200, 210)
    metal_dark = (140, 140, 150)
    
    # Blade 1
    blade1_points = [
        (cx - size * 0.1, cy + size * 0.2),
        (cx - size * 0.35, cy - size * 0.5),
        (cx - size * 0.25, cy - size * 0.52),
        (cx - size * 0.05, cy + size * 0.15),
    ]
    pygame.draw.polygon(temp_surface, metal, blade1_points)
    pygame.draw.polygon(temp_surface, metal_dark, blade1_points, 2)
    
    # Blade 2
    blade2_points = [
        (cx + size * 0.1, cy + size * 0.2),
        (cx + size * 0.35, cy - size * 0.5),
        (cx + size * 0.25, cy - size * 0.52),
        (cx + size * 0.05, cy + size * 0.15),
    ]
    pygame.draw.polygon(temp_surface, metal, blade2_points)
    pygame.draw.polygon(temp_surface, metal_dark, blade2_points, 2)
    
    # Handle rings
    pygame.draw.ellipse(temp_surface, scissors_color,
                       (cx - size * 0.35, cy + size * 0.1, size * 0.35, size * 0.35))
    pygame.draw.ellipse(temp_surface, darker,
                       (cx - size * 0.25, cy + size * 0.17, size * 0.15, size * 0.2))
    
    pygame.draw.ellipse(temp_surface, scissors_color,
                       (cx, cy + size * 0.1, size * 0.35, size * 0.35))
    pygame.draw.ellipse(temp_surface, darker,
                       (cx + size * 0.1, cy + size * 0.17, size * 0.15, size * 0.2))
    
    # Center pivot
    pygame.draw.circle(temp_surface, metal_dark, (int(cx), int(cy + size * 0.1)), int(size * 0.08))
    pygame.draw.circle(temp_surface, metal, (int(cx), int(cy + size * 0.1)), int(size * 0.05))
    
    # Rotate and blit
    if angle != 0:
        temp_surface = pygame.transform.rotate(temp_surface, angle)
    rect = temp_surface.get_rect(center=(x, y))
    surface.blit(temp_surface, rect)


def draw_choice_icon(surface: pygame.Surface, choice: Choice, x: int, y: int,
                     size: int, color: Tuple[int, int, int], angle: float = 0):
    """Draw the appropriate icon for a choice."""
    if choice == Choice.ROCK:
        draw_rock(surface, x, y, size, color, angle)
    elif choice == Choice.PAPER:
        draw_paper(surface, x, y, size, color, angle)
    elif choice == Choice.SCISSORS:
        draw_scissors(surface, x, y, size, color, angle)


def draw_gradient_bg(surface: pygame.Surface):
    """Draw a gradient background."""
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(COLORS['bg_dark'][0] * (1 - ratio) + COLORS['bg_gradient'][0] * ratio)
        g = int(COLORS['bg_dark'][1] * (1 - ratio) + COLORS['bg_gradient'][1] * ratio)
        b = int(COLORS['bg_dark'][2] * (1 - ratio) + COLORS['bg_gradient'][2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))


def create_background_surface() -> pygame.Surface:
    """Create and return a pre-rendered background surface."""
    bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    draw_gradient_bg(bg_surface)
    return bg_surface


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
    num_text = constants.FONT_MEDIUM.render(f"P{player.id}", True, num_color)
    num_rect = num_text.get_rect(center=(cx, 35))
    temp_surface.blit(num_text, num_rect)
    
    if not player.joined:
        # Show join prompt with ready key (rock/left key)
        ready_key_name = pygame.key.name(player.rock_key).upper()
        join_text = constants.FONT_SMALL.render(f"Press {ready_key_name}", True, (150, 150, 150))
        join_rect = join_text.get_rect(center=(cx, 80))
        temp_surface.blit(join_text, join_rect)
    elif is_eliminated:
        # Show eliminated text
        elim_text = constants.FONT_SMALL.render("ELIMINATED", True, (200, 60, 60))
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
            hint_text = constants.FONT_TINY.render(f"{r_key}  {p_key}  {s_key}", True, (180, 180, 180))
        else:
            hint_text = constants.FONT_TINY.render("LOCKED IN!", True, COLORS['green'])
        
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


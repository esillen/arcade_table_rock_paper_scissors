"""
Rock Paper Scissors icon rendering using vector graphics.
"""

import pygame
import math
from typing import Tuple

from core.enums import Choice


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


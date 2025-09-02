"""
Design System Module
Contains all design tokens including colors, fonts, spacing, and styling configurations.
"""

import tkinter as tk
from tkinter import ttk


class DesignSystem:
    """Centralized design system for the Football Scores Pro application."""
    
    def __init__(self):
        self.setup_colors()
        self.setup_fonts()
        self.setup_spacing()
        self.setup_ttk_styles()
    
    def setup_colors(self):
        """Setup modern color palette"""
        self.colors = {
            # Primary Colors
            'primary': '#0066FF',           # Electric Blue
            'success': '#00C851',           # Stadium Green
            'live': '#FF1744',              # Live Red
            'warning': '#FFD700',           # Championship Gold
            'danger': '#FF6B35',            # Sunset Orange
            
            # Background Colors
            'bg_primary': '#F8F9FA',        # Cloud White background
            'bg_secondary': '#FFFFFF',       # Pure white
            'bg_card': '#FFFFFF',           # Card backgrounds
            'bg_sidebar': '#FFFFFF',        # Sidebar background
            'bg_header': '#1B1B2F',         # Midnight Navy
            
            # Text Colors
            'text_primary': '#1B1B2F',      # Midnight Navy
            'text_secondary': '#6C757D',    # Steel Gray
            'text_muted': '#ADB5BD',        # Light gray
            'text_white': '#FFFFFF',        # White text
            
            # State Colors
            'finished': '#4CAF50',          # Victory Green
            'upcoming': '#3F51B5',          # Upcoming Indigo
            'draw': '#FFC107',              # Draw Amber
            
            # UI Colors
            'border': '#DEE2E6',            # Light border
            'shadow': 'rgba(0,0,0,0.1)',    # Subtle shadow
            'hover': '#F8F9FA',             # Hover state
            'active': '#E3F2FD',            # Active state
        }
    
    def setup_fonts(self):
        """Setup typography scale"""
        self.fonts = {
            'display_large': ('Inter', 32, 'bold'),
            'display_medium': ('Inter', 24, 'bold'),
            'headline': ('Inter', 18, 'normal'),
            'body_large': ('Inter', 16, 'normal'),
            'body_medium': ('Inter', 14, 'normal'),
            'caption': ('Inter', 12, 'normal'),
            'label': ('Inter', 11, 'bold'),
        }
    
    def setup_spacing(self):
        """Setup spacing system (8px grid)"""
        self.spacing = {
            'xs': 4,
            'sm': 8,
            'md': 16,
            'lg': 24,
            'xl': 32,
            'xxl': 48
        }
    
    def setup_ttk_styles(self):
        """Configure modern ttk styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Modern button styles
        self.style.configure('Modern.TButton',
                           font=self.fonts['body_medium'],
                           borderwidth=0,
                           focuscolor='none',
                           relief='flat',
                           padding=(20, 10))
        
        self.style.map('Modern.TButton',
                     background=[('active', self.colors['primary']),
                                ('pressed', self.colors['primary'])])
        
        # Primary button style
        self.style.configure('Primary.TButton',
                           font=self.fonts['body_medium'],
                           background=self.colors['primary'],
                           foreground=self.colors['text_white'],
                           borderwidth=0,
                           focuscolor='none',
                           relief='flat',
                           padding=(24, 12))
        
        # Secondary button style  
        self.style.configure('Secondary.TButton',
                           font=self.fonts['body_medium'],
                           background=self.colors['bg_card'],
                           foreground=self.colors['primary'],
                           borderwidth=1,
                           focuscolor='none',
                           relief='solid',
                           padding=(20, 10))
        
        # Search entry style
        self.style.configure('Search.TEntry',
                           font=self.fonts['body_medium'],
                           borderwidth=0,
                           relief='flat',
                           padding=(16, 12))
    
    def get_section_color(self, section_type):
        """Get color for section type"""
        colors = {
            'live': self.colors['live'],
            'finished': self.colors['finished'],
            'upcoming': self.colors['upcoming']
        }
        return colors.get(section_type, self.colors['primary'])
    
    def truncate_team_name(self, name, max_length=20):
        """Truncate team name for display"""
        return name[:max_length] + '...' if len(name) > max_length else name

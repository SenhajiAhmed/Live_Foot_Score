"""
Design System Module
Contains all design tokens including colors, fonts, spacing, and styling configurations.
"""

import tkinter as tk
from tkinter import ttk


class DesignSystem:
    """Centralized design system for the Football Scores Pro application."""
    
    def __init__(self, theme='dark'):
        self._theme = theme
        self._callbacks = []
        self.setup_colors()
        self.setup_fonts()
        self.setup_spacing()
        self.setup_ttk_styles()
    
    @property
    def current_theme(self):
        return self._theme
    
    @current_theme.setter
    def current_theme(self, value):
        if value != self._theme:
            self._theme = value
            self.setup_colors()
            self.setup_ttk_styles()
            self.notify_theme_change()
    
    def register_theme_change_callback(self, callback):
        """Register a callback to be called when theme changes"""
        if callback not in self._callbacks:
            self._callbacks.append(callback)
    
    def unregister_theme_change_callback(self, callback):
        """Unregister a theme change callback"""
        if callback in self._callbacks:
            self._callbacks.remove(callback)
    
    def notify_theme_change(self):
        """Notify all registered callbacks of theme change"""
        for callback in self._callbacks[:]:  # Create a copy to allow modification during iteration
            try:
                callback()
            except Exception as e:
                print(f"Error in theme change callback: {e}")
    
    def setup_colors(self):
        """Setup modern color palette based on current theme"""
        if self.current_theme == 'dark':
            self.colors = {
                # Primary Colors
                'primary': '#4A9EFF',           # Lighter Blue for dark mode
                'success': '#00C851',           # Stadium Green
                'live': '#FF1744',              # Live Red
                'warning': '#FFD700',           # Championship Gold
                'danger': '#FF6B35',            # Sunset Orange
                
                # Background Colors
                'bg_primary': '#1A1A1A',        # Dark background
                'bg_secondary': '#2D2D2D',       # Darker secondary
                'bg_card': '#2D2D2D',           # Dark card backgrounds
                'bg_sidebar': '#2D2D2D',        # Dark sidebar background
                'bg_header': '#1B1B2F',         # Midnight Navy
                
                # Text Colors
                'text_primary': '#FFFFFF',      # White text
                'text_secondary': '#B0B0B0',    # Light gray
                'text_muted': '#808080',        # Medium gray
                'text_white': '#FFFFFF',        # White text
                
                # State Colors
                'finished': '#4CAF50',          # Victory Green
                'upcoming': '#3F51B5',          # Upcoming Indigo
                'draw': '#FFC107',              # Draw Amber
                
                # UI Colors
                'border': '#404040',            # Dark border
                'shadow': 'rgba(0,0,0,0.3)',    # Darker shadow
                'hover': '#3A3A3A',             # Dark hover state
                'active': '#1E3A5F',            # Dark active state
            }
        else:  # Light theme
            self.colors = {
                # Primary Colors
                'primary': '#1a73e8',           # Google Blue
                'success': '#0b8043',           # Darker Green
                'live': '#d93025',              # Google Red
                'warning': '#e37400',           # Orange
                'danger': '#d93025',            # Google Red
                
                # Background Colors
                'bg_primary': '#f8f9fa',        # Light gray background
                'bg_secondary': '#ffffff',       # Pure white
                'bg_card': '#ffffff',           # Card backgrounds
                'bg_sidebar': '#f1f3f4',       # Light gray sidebar
                'bg_header': '#1a73e8',         # Blue header
                
                # Text Colors
                'text_primary': '#202124',      # Almost black
                'text_secondary': '#5f6368',    # Dark gray
                'text_muted': '#9aa0a6',        # Medium gray
                'text_white': '#ffffff',        # White text
                
                # State Colors
                'finished': '#0b8043',          # Dark Green
                'upcoming': '#1a73e8',          # Blue
                'draw': '#e37400',              # Orange
                
                # UI Colors
                'border': '#dadce0',            # Light gray border
                'shadow': 'rgba(60,64,67,0.15)',# Subtle shadow
                'hover': '#f1f3f4',             # Light gray hover
                'active': '#e8f0fe',            # Light blue active
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
    
    def switch_theme(self, theme):
        """Switch between light and dark themes"""
        if theme in ['light', 'dark']:
            self.current_theme = theme
            self.setup_colors()
            self.setup_ttk_styles()
            return True
        return False
    
    def get_theme(self):
        """Get current theme"""
        return self.current_theme
    
    def is_dark_theme(self):
        """Check if current theme is dark"""
        return self.current_theme == 'dark'

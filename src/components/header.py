"""
Header Component Module
Contains the modern header with logo, title, and live indicator
"""

import tkinter as tk
from datetime import datetime


class Header:
    """Modern header component with gradient background"""
    
    def __init__(self, parent, design_system):
        self.parent = parent
        self.ds = design_system
        self.create_header()
    
    def create_header(self):
        """Create modern header with gradient background"""
        self.header = tk.Frame(
            self.parent,
            bg=self.ds.colors['bg_header'],
            height=80
        )
        self.header.pack(fill=tk.X)
        self.header.pack_propagate(False)
        
        # Left section with logo and title
        left_section = tk.Frame(self.header, bg=self.ds.colors['bg_header'])
        left_section.pack(side=tk.LEFT, fill=tk.Y, padx=self.ds.spacing['xl'])
        
        # Logo and title container
        logo_container = tk.Frame(left_section, bg=self.ds.colors['bg_header'])
        logo_container.pack(expand=True)
        
        # Modern logo
        logo_label = tk.Label(
            logo_container,
            text="⚽",
            font=('Inter', 28),
            bg=self.ds.colors['bg_header'],
            fg=self.ds.colors['success']
        )
        logo_label.pack(side=tk.LEFT, padx=(0, self.ds.spacing['md']))
        
        # App title with modern typography
        title_label = tk.Label(
            logo_container,
            text="FOOTBALL SCORES PRO",
            font=self.ds.fonts['display_medium'],
            bg=self.ds.colors['bg_header'],
            fg=self.ds.colors['text_white']
        )
        title_label.pack(side=tk.LEFT)
        
        # Right section with date and live indicator
        right_section = tk.Frame(self.header, bg=self.ds.colors['bg_header'])
        right_section.pack(side=tk.RIGHT, fill=tk.Y, padx=self.ds.spacing['xl'])
        
        # Live indicator
        self.live_indicator = tk.Frame(right_section, bg=self.ds.colors['bg_header'])
        self.live_indicator.pack(side=tk.RIGHT, padx=(self.ds.spacing['lg'], 0))
        
        self.live_dot = tk.Label(
            self.live_indicator,
            text="●",
            font=self.ds.fonts['body_large'],
            bg=self.ds.colors['bg_header'],
            fg=self.ds.colors['live']
        )
        self.live_dot.pack(side=tk.LEFT, padx=(0, self.ds.spacing['sm']))
        
        tk.Label(
            self.live_indicator,
            text="LIVE",
            font=self.ds.fonts['label'],
            bg=self.ds.colors['bg_header'],
            fg=self.ds.colors['text_white']
        ).pack(side=tk.LEFT)
        
        # Date display
        self.date_var = tk.StringVar()
        self.date_var.set(datetime.now().strftime("%A, %B %d, %Y"))
        
        date_label = tk.Label(
            right_section,
            textvariable=self.date_var,
            font=self.ds.fonts['body_medium'],
            bg=self.ds.colors['bg_header'],
            fg=self.ds.colors['text_muted']
        )
        date_label.pack(side=tk.RIGHT, padx=(0, self.ds.spacing['lg']))
    
    def animate_live_indicator(self, animation_active):
        """Animate live indicator in header"""
        if animation_active:
            current_color = self.live_dot.cget('fg')
            new_color = self.ds.colors['bg_header'] if current_color == self.ds.colors['live'] else self.ds.colors['live']
            self.live_dot.config(fg=new_color)
        
        return animation_active  # Return for next animation cycle

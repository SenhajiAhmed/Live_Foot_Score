"""
Header Component Module
Contains the modern header with logo, title, and live indicator.
"""

import tkinter as tk
from datetime import datetime


class Header:
    """Modern header component with logo, title, and live indicator."""
    
    def __init__(self, parent, design_system):
        self.parent = parent
        self.design = design_system
        self.animation_active = True
        
        self.create_header()
        self.start_live_animations()
    
    def create_header(self):
        """Create modern header with gradient background"""
        # Store header frame reference for theme updates
        self.header = tk.Frame(
            self.parent,
            bg=self.design.colors['bg_header'],
            height=80
        )
        self.header.pack(fill=tk.X)
        self.header.pack_propagate(False)
        
        # Store references to themed widgets
        self.themed_widgets = []
        
        # Left section with logo and title
        self.left_section = tk.Frame(self.header, bg=self.design.colors['bg_header'])
        self.left_section.pack(side=tk.LEFT, fill=tk.Y, padx=self.design.spacing['xl'])
        self.themed_widgets.append(self.left_section)
        
        # Logo and title container
        self.logo_container = tk.Frame(self.left_section, bg=self.design.colors['bg_header'])
        self.logo_container.pack(expand=True)
        self.themed_widgets.append(self.logo_container)
        
        # Modern logo
        self.logo_label = tk.Label(
            self.logo_container,
            text="⚽",
            font=('Inter', 28),
            bg=self.design.colors['bg_header'],
            fg=self.design.colors['success']
        )
        self.logo_label.pack(side=tk.LEFT, padx=(0, self.design.spacing['md']))
        self.themed_widgets.append(self.logo_label)
        
        # App title with modern typography
        self.title_label = tk.Label(
            self.logo_container,
            text="FOOTBALL SCORES PRO",
            font=self.design.fonts['display_medium'],
            bg=self.design.colors['bg_header'],
            fg=self.design.colors['text_white']
        )
        self.title_label.pack(side=tk.LEFT)
        self.themed_widgets.append(self.title_label)
        
        # Right section with date and live indicator
        self.right_section = tk.Frame(self.header, bg=self.design.colors['bg_header'])
        self.right_section.pack(side=tk.RIGHT, fill=tk.Y, padx=self.design.spacing['xl'])
        self.themed_widgets.append(self.right_section)
        
        # Live indicator
        self.live_indicator = tk.Frame(self.right_section, bg=self.design.colors['bg_header'])
        self.live_indicator.pack(side=tk.RIGHT, padx=(self.design.spacing['lg'], 0))
        self.themed_widgets.append(self.live_indicator)
        
        self.live_dot = tk.Label(
            self.live_indicator,
            text="●",
            font=self.design.fonts['body_large'],
            bg=self.design.colors['bg_header'],
            fg=self.design.colors['live']
        )
        self.live_dot.pack(side=tk.LEFT, padx=(0, self.design.spacing['sm']))
        
        tk.Label(
            self.live_indicator,
            text="LIVE",
            font=self.design.fonts['label'],
            bg=self.design.colors['bg_header'],
            fg=self.design.colors['text_white']
        ).pack(side=tk.LEFT)
        
        # Date display
        self.date_var = tk.StringVar()
        self.date_var.set(datetime.now().strftime("%A, %B %d, %Y"))
        
        date_label = tk.Label(
            self.right_section,
            textvariable=self.date_var,
            font=self.design.fonts['body_medium'],
            bg=self.design.colors['bg_header'],
            fg=self.design.colors['text_muted']
        )
        date_label.pack(side=tk.RIGHT, padx=(0, self.design.spacing['lg']))
    
    def start_live_animations(self):
        """Start background animations for live elements"""
        self.animate_live_indicator()
        
    def update_theme(self, design_system):
        """Update theme colors for all widgets"""
        self.design = design_system
        
        # Update header background
        self.header.config(bg=self.design.colors['bg_header'])
        
        # Update all themed widgets
        for widget in self.themed_widgets:
            try:
                if isinstance(widget, tk.Frame):
                    widget.config(bg=self.design.colors['bg_header'])
                elif isinstance(widget, tk.Label):
                    if hasattr(self, 'logo_label') and widget == self.logo_label:
                        widget.config(
                            bg=self.design.colors['bg_header'],
                            fg=self.design.colors['success']
                        )
                    elif hasattr(self, 'title_label') and widget == self.title_label:
                        widget.config(
                            bg=self.design.colors['bg_header'],
                            fg=self.design.colors['text_white']
                        )
                    else:
                        widget.config(
                            bg=self.design.colors['bg_header'],
                            fg=self.design.colors['text_white']
                        )
            except Exception as e:
                print(f"Error updating widget theme: {e}")
        
        # Update live indicator if it exists
        if hasattr(self, 'live_dot'):
            self.live_dot.config(
                bg=self.design.colors['bg_header'],
                fg=self.design.colors['live']
            )
        
        # Update all child widgets
        for child in self.header.winfo_children():
            self.update_widget_theme(child)
    
    def animate_live_indicator(self):
        """Animate live indicator in header"""
        if self.animation_active:
            current_color = self.live_dot.cget('fg')
            new_color = (self.design.colors['bg_header'] 
                        if current_color == self.design.colors['live'] 
                        else self.design.colors['live'])
            self.live_dot.config(fg=new_color)
            
        # Schedule next animation
        self.parent.after(1000, self.animate_live_indicator)
    
    def update_widget_theme(self, widget):
        """Recursively update widget theme"""
        try:
            if isinstance(widget, tk.Label):
                text = widget.cget('text')
                if text == "FOOTBALL SCORES PRO" or text == "LIVE":
                    widget.config(
                        bg=self.design.colors['bg_header'],
                        fg=self.design.colors['text_white']
                    )
                elif hasattr(self, 'date_var') and widget.cget('textvariable') == self.date_var:
                    widget.config(
                        bg=self.design.colors['bg_header'],
                        fg=self.design.colors['text_white']
                    )
                elif widget not in self.themed_widgets:  # Only update if not already handled
                    widget.config(
                        bg=self.design.colors['bg_header'],
                        fg=self.design.colors['text_white']
                    )
            
            # Recursively update child widgets
            for child in widget.winfo_children():
                self.update_widget_theme(child)
        except Exception as e:
            print(f"Error updating widget theme: {e}")
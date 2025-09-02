"""
Status Bar Component Module
Contains the modern status bar with status text and match count.
"""

import tkinter as tk


class StatusBar:
    """Modern status bar component with status text and match count."""
    
    def __init__(self, parent, design_system):
        self.parent = parent
        self.design = design_system
        
        self.create_status_bar()
    
    def create_status_bar(self):
        """Create modern status bar"""
        status_container = tk.Frame(
            self.parent,
            bg=self.design.colors['primary'],
            height=40
        )
        status_container.pack(side=tk.BOTTOM, fill=tk.X)
        status_container.pack_propagate(False)
        
        # Status content
        status_content = tk.Frame(status_container, bg=self.design.colors['primary'])
        status_content.pack(expand=True, padx=self.design.spacing['xl'])
        
        # Status text
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(
            status_content,
            textvariable=self.status_var,
            font=self.design.fonts['body_medium'],
            fg=self.design.colors['text_white'],
            bg=self.design.colors['primary'],
            anchor='w'
        )
        self.status_bar.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.status_var.set("Ready")
        
        # Match count
        self.match_count_label = tk.Label(
            status_content,
            text="0 matches",
            font=self.design.fonts['caption'],
            fg=self.design.colors['text_white'],
            bg=self.design.colors['primary'],
            anchor='e'
        )
        self.match_count_label.pack(side=tk.RIGHT)
    
    def update_status(self, message):
        """Update status message"""
        self.status_var.set(message)
    
    def update_match_count(self, count):
        """Update match count display"""
        self.match_count_label.config(text=f"{count} matches")

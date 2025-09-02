"""
Content Component Module
Contains the main content area with scrolling and match display
"""

import tkinter as tk
from tkinter import ttk


class Content:
    """Modern content area component"""
    
    def __init__(self, parent, design_system):
        self.parent = parent
        self.ds = design_system
        self.create_content()
    
    def create_content(self):
        """Create modern content area"""
        content = tk.Frame(
            self.parent, 
            bg=self.ds.colors['bg_card'],
            relief=tk.FLAT,
            bd=1,
            highlightbackground=self.ds.colors['border'],
            highlightthickness=1
        )
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Content header
        header = tk.Frame(content, bg=self.ds.colors['bg_card'], height=80)
        header.pack(fill=tk.X, padx=self.ds.spacing['xl'], pady=self.ds.spacing['lg'])
        header.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header, bg=self.ds.colors['bg_card'])
        header_content.pack(expand=True)
        
        self.content_title = tk.Label(
            header_content,
            text="Live Matches",
            font=self.ds.fonts['display_medium'],
            fg=self.ds.colors['text_primary'],
            bg=self.ds.colors['bg_card'],
            anchor='w'
        )
        self.content_title.pack(fill=tk.X)
        
        # Subtitle
        self.content_subtitle = tk.Label(
            header_content,
            text="Real-time football scores and updates",
            font=self.ds.fonts['body_medium'],
            fg=self.ds.colors['text_secondary'],
            bg=self.ds.colors['bg_card'],
            anchor='w'
        )
        self.content_subtitle.pack(fill=tk.X, pady=(self.ds.spacing['xs'], 0))
        
        # Matches container with modern scrolling
        self.matches_container = tk.Frame(content, bg=self.ds.colors['bg_card'])
        self.matches_container.pack(fill=tk.BOTH, expand=True, padx=self.ds.spacing['xl'], pady=(0, self.ds.spacing['lg']))
        
        # Custom scrollable area
        self.setup_modern_scrollable_area()
        
        # Show modern empty state
        self.show_modern_empty_state()
    
    def setup_modern_scrollable_area(self):
        """Setup modern scrollable area with custom styling"""
        # Canvas for scrolling
        self.canvas = tk.Canvas(
            self.matches_container,
            bg=self.ds.colors['bg_card'],
            bd=0,
            highlightthickness=0
        )
        
        # Modern scrollbar
        scrollbar = ttk.Scrollbar(
            self.matches_container,
            orient=tk.VERTICAL,
            command=self.canvas.yview
        )
        
        # Scrollable frame
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.ds.colors['bg_card'])
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Smooth mousewheel scrolling
        self.canvas.bind_all("<MouseWheel>", self.smooth_scroll)
    
    def show_modern_empty_state(self, message="No matches available", subtitle="Click 'Fetch Matches' to get the latest scores"):
        """Show modern empty state"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        empty_container = tk.Frame(self.scrollable_frame, bg=self.ds.colors['bg_card'])
        empty_container.pack(expand=True, fill=tk.BOTH)
        
        # Center the empty state
        empty_frame = tk.Frame(empty_container, bg=self.ds.colors['bg_card'])
        empty_frame.pack(expand=True)
        
        # Large icon
        tk.Label(
            empty_frame,
            text="⚽",
            font=('Inter', 64),
            fg=self.ds.colors['text_muted'],
            bg=self.ds.colors['bg_card']
        ).pack(pady=(0, self.ds.spacing['lg']))
        
        # Main message
        tk.Label(
            empty_frame,
            text=message,
            font=self.ds.fonts['headline'],
            fg=self.ds.colors['text_secondary'],
            bg=self.ds.colors['bg_card']
        ).pack(pady=(0, self.ds.spacing['sm']))
        
        # Subtitle
        tk.Label(
            empty_frame,
            text=subtitle,
            font=self.ds.fonts['body_medium'],
            fg=self.ds.colors['text_muted'],
            bg=self.ds.colors['bg_card']
        ).pack()
    
    def show_modern_loading_state(self):
        """Show modern loading state with skeleton screens"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        loading_frame = tk.Frame(self.scrollable_frame, bg=self.ds.colors['bg_card'])
        loading_frame.pack(fill=tk.BOTH, expand=True, padx=self.ds.spacing['lg'], pady=self.ds.spacing['lg'])
        
        # Create skeleton cards
        for i in range(3):
            self.create_skeleton_card(loading_frame)
    
    def create_skeleton_card(self, parent):
        """Create skeleton loading card"""
        skeleton_card = tk.Frame(
            parent,
            bg=self.ds.colors['bg_primary'],
            relief=tk.FLAT,
            bd=1,
            highlightbackground=self.ds.colors['border'],
            highlightthickness=1
        )
        skeleton_card.pack(fill=tk.X, pady=self.ds.spacing['sm'])
        
        # Skeleton content
        content = tk.Frame(skeleton_card, bg=self.ds.colors['bg_primary'])
        content.pack(fill=tk.X, padx=self.ds.spacing['lg'], pady=self.ds.spacing['lg'])
        
        # Tournament name skeleton
        tk.Frame(
            content,
            bg=self.ds.colors['border'],
            height=20,
            width=200
        ).pack(anchor='w', pady=(0, self.ds.spacing['md']))
        
        # Match skeleton
        match_frame = tk.Frame(content, bg=self.ds.colors['bg_primary'])
        match_frame.pack(fill=tk.X)
        
        for _ in range(2):
            tk.Frame(
                match_frame,
                bg=self.ds.colors['border'],
                height=15,
                width=150
            ).pack(anchor='w', pady=self.ds.spacing['xs'])
    
    def smooth_scroll(self, event):
        """Smooth scrolling for canvas"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def clear_content(self):
        """Clear all content from scrollable frame"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
    
    def update_title(self, title, subtitle):
        """Update content title and subtitle"""
        self.content_title.config(text=title)
        self.content_subtitle.config(text=subtitle)

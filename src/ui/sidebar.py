"""
Sidebar Component Module
Contains the modern sidebar with navigation, actions, and status.
"""

import tkinter as tk


class Sidebar:
    """Modern sidebar component with navigation, actions, and status."""
    
    def __init__(self, parent, design_system, callbacks):
        self.parent = parent
        self.design = design_system
        self.callbacks = callbacks
        self.nav_buttons = []
        
        # Validate callbacks
        self.validate_callbacks()
        
        self.create_sidebar()
    
    def validate_callbacks(self):
        """Validate that all required callbacks are present"""
        required_callbacks = [
            'fetch_matches', 'stop_fetching', 'show_live_matches', 
            'show_fixtures', 'show_finished', 'show_settings'
        ]
        
        for callback_name in required_callbacks:
            if callback_name not in self.callbacks or self.callbacks[callback_name] is None:
                print(f"Warning: Missing callback '{callback_name}'")
                # Create a dummy callback that shows a message
                self.callbacks[callback_name] = lambda: print(f"Callback '{callback_name}' not implemented")
    
    def create_sidebar(self):
        """Create modern sidebar with card design"""
        # Sidebar container
        sidebar_container = tk.Frame(
            self.parent,
            bg=self.design.colors['bg_secondary'],
            width=300,
            height=800
        )
        sidebar_container.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        sidebar_container.pack_propagate(False)
        
        # Sidebar card
        self.sidebar = tk.Frame(
            sidebar_container,
            bg=self.design.colors['bg_sidebar'],
            width=280,
            height=800
        )
        self.sidebar.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add navigation and other sections
        self.create_modern_search()
        self.create_modern_navigation()
        self.create_modern_actions()
        self.create_sidebar_status()
    
    def create_modern_search(self):
        """Create modern search bar"""
        search_section = tk.Frame(
            self.sidebar, 
            bg=self.design.colors['bg_sidebar']
        )
        search_section.pack(fill=tk.X, padx=self.design.spacing['lg'], pady=self.design.spacing['lg'])
        
        # Search container with pill shape
        search_container = tk.Frame(
            search_section,
            bg=self.design.colors['bg_primary'],
            relief=tk.FLAT,
            bd=0
        )
        search_container.pack(fill=tk.X, ipady=self.design.spacing['sm'])
        
        # Search icon
        search_icon = tk.Label(
            search_container,
            text="🔍",
            font=self.design.fonts['body_medium'],
            bg=self.design.colors['bg_primary'],
            fg=self.design.colors['text_secondary']
        )
        search_icon.pack(side=tk.LEFT, padx=(self.design.spacing['md'], self.design.spacing['sm']))
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_container,
            textvariable=self.search_var,
            font=self.design.fonts['body_medium'],
            bg=self.design.colors['bg_primary'],
            fg=self.design.colors['text_primary'],
            border=0,
            relief=tk.FLAT
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, self.design.spacing['md']))
        
        # Placeholder behavior
        self.search_entry.insert(0, "Search matches...")
        self.search_entry.bind('<FocusIn>', self.on_search_focus_in)
        self.search_entry.bind('<FocusOut>', self.on_search_focus_out)
    
    def create_modern_navigation(self):
        """Create modern navigation menu"""
        nav_section = tk.Frame(self.sidebar, bg=self.design.colors['bg_sidebar'])
        nav_section.pack(fill=tk.X, pady=self.design.spacing['md'])
        
        # Navigation items with modern styling
        nav_items = [
            ("📊", "Live Matches", self.callbacks['show_live_matches'], True),
            ("📅", "Fixtures", self.callbacks['show_fixtures'], False),
            ("🏁", "Finished", self.callbacks['show_finished'], False),
            ("⚙️", "Settings", self.callbacks['show_settings'], False)
        ]
        
        self.nav_buttons = []
        for icon, text, command, active in nav_items:
            btn_frame = tk.Frame(nav_section, bg=self.design.colors['bg_sidebar'])
            btn_frame.pack(fill=tk.X, padx=self.design.spacing['md'], pady=self.design.spacing['xs'])
            
            if active:
                btn_frame.config(bg=self.design.colors['active'])
                
            btn = tk.Button(
                btn_frame,
                text=f"{icon}  {text}",
                font=self.design.fonts['body_medium'],
                bg=self.design.colors['active'] if active else self.design.colors['bg_sidebar'],
                fg=self.design.colors['primary'] if active else self.design.colors['text_primary'],
                bd=0,
                relief=tk.FLAT,
                anchor='w',
                padx=self.design.spacing['lg'],
                pady=self.design.spacing['md'],
                command=command,
                cursor='hand2'
            )
            btn.pack(fill=tk.X)
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn, f=btn_frame: self.nav_hover_enter(b, f))
            btn.bind('<Leave>', lambda e, b=btn, f=btn_frame, a=active: self.nav_hover_leave(b, f, a))
            
            self.nav_buttons.append((btn, btn_frame, active))
        
        # Separator
        separator = tk.Frame(
            nav_section, 
            bg=self.design.colors['border'], 
            height=1
        )
        separator.pack(fill=tk.X, padx=self.design.spacing['lg'], pady=self.design.spacing['lg'])
    
    def create_modern_actions(self):
        """Create modern action buttons"""
        action_section = tk.Frame(self.sidebar, bg=self.design.colors['bg_sidebar'])
        action_section.pack(fill=tk.X, padx=self.design.spacing['lg'], pady=self.design.spacing['md'])
        
        # Fetch button with modern styling
        self.fetch_btn = tk.Button(
            action_section,
            text="🔄  Fetch Matches",
            font=self.design.fonts['body_medium'],
            bg=self.design.colors['success'],
            fg=self.design.colors['text_white'],
            bd=0,
            relief=tk.FLAT,
            padx=self.design.spacing['lg'],
            pady=self.design.spacing['md'],
            command=self.callbacks['fetch_matches'],
            cursor='hand2'
        )
        self.fetch_btn.pack(fill=tk.X, pady=(0, self.design.spacing['sm']))
        
        # Stop button
        self.stop_btn = tk.Button(
            action_section,
            text="⏹  Stop",
            font=self.design.fonts['body_medium'],
            bg=self.design.colors['bg_card'],
            fg=self.design.colors['danger'],
            bd=1,
            relief=tk.SOLID,
            padx=self.design.spacing['lg'],
            pady=self.design.spacing['md'],
            command=self.callbacks['stop_fetching'],
            state=tk.DISABLED,
            cursor='hand2'
        )
        self.stop_btn.pack(fill=tk.X)
        
        # Button hover effects
        self.setup_button_hover_effects()
    
    def create_sidebar_status(self):
        """Create sidebar status section"""
        status_section = tk.Frame(self.sidebar, bg=self.design.colors['bg_sidebar'])
        status_section.pack(side=tk.BOTTOM, fill=tk.X, padx=self.design.spacing['lg'], pady=self.design.spacing['lg'])
        
        # Status indicator
        status_container = tk.Frame(
            status_section,
            bg=self.design.colors['bg_primary'],
            relief=tk.FLAT
        )
        status_container.pack(fill=tk.X, pady=self.design.spacing['sm'])
        
        # Status dot
        self.status_dot = tk.Label(
            status_container,
            text="●",
            font=self.design.fonts['body_medium'],
            bg=self.design.colors['bg_primary'],
            fg=self.design.colors['success']
        )
        self.status_dot.pack(side=tk.LEFT, padx=(self.design.spacing['md'], self.design.spacing['sm']))
        
        # Status text
        self.status_label = tk.Label(
            status_container,
            text="Ready to fetch matches",
            font=self.design.fonts['caption'],
            fg=self.design.colors['text_secondary'],
            bg=self.design.colors['bg_primary'],
            anchor='w'
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, self.design.spacing['md']))
    
    def setup_button_hover_effects(self):
        """Setup hover effects for buttons"""
        def fetch_hover_enter(e):
            self.fetch_btn.config(bg=self.design.colors['text_primary'])
        
        def fetch_hover_leave(e):
            if self.fetch_btn['state'] != tk.DISABLED:
                self.fetch_btn.config(bg=self.design.colors['success'])
        
        def stop_hover_enter(e):
            if self.stop_btn['state'] != tk.DISABLED:
                self.stop_btn.config(bg=self.design.colors['text_primary'])
        
        def stop_hover_leave(e):
            if self.stop_btn['state'] != tk.DISABLED:
                self.stop_btn.config(bg=self.design.colors['danger'])
        
        self.fetch_btn.bind('<Enter>', fetch_hover_enter)
        self.fetch_btn.bind('<Leave>', fetch_hover_leave)
        self.stop_btn.bind('<Enter>', stop_hover_enter)
        self.stop_btn.bind('<Leave>', stop_hover_leave)
    
    def nav_hover_enter(self, button, frame):
        """Navigation hover enter effect"""
        if button.cget('bg') != self.design.colors['active']:
            button.config(bg=self.design.colors['hover'])
            frame.config(bg=self.design.colors['hover'])
    
    def nav_hover_leave(self, button, frame, is_active):
        """Navigation hover leave effect"""
        if is_active:
            button.config(bg=self.design.colors['active'])
            frame.config(bg=self.design.colors['active'])
        else:
            button.config(bg=self.design.colors['bg_sidebar'])
            frame.config(bg=self.design.colors['bg_sidebar'])
    
    def on_search_focus_in(self, event):
        """Handle search focus in"""
        if event.widget.get() == "Search matches...":
            event.widget.delete(0, tk.END)
            event.widget.config(fg=self.design.colors['text_primary'])
    
    def on_search_focus_out(self, event):
        """Handle search focus out"""
        if not event.widget.get():
            event.widget.insert(0, "Search matches...")
            event.widget.config(fg=self.design.colors['text_muted'])
    
    def update_nav_selection(self, active_index):
        """Update navigation selection styling"""
        for i, (btn, frame, _) in enumerate(self.nav_buttons):
            if i == active_index:
                btn.config(bg=self.design.colors['active'], fg=self.design.colors['primary'])
                frame.config(bg=self.design.colors['active'])
                self.nav_buttons[i] = (btn, frame, True)
            else:
                btn.config(bg=self.design.colors['bg_sidebar'], fg=self.design.colors['text_primary'])
                frame.config(bg=self.design.colors['bg_sidebar'])
                self.nav_buttons[i] = (btn, frame, False)
    
    def update_status(self, message, color, indicator="●"):
        """Update status with modern styling"""
        self.status_label.config(text=message, fg=color)
        self.status_dot.config(fg=color, text=indicator)
    
    def set_fetch_button_state(self, enabled):
        """Set fetch button state"""
        if enabled:
            self.fetch_btn.config(state=tk.NORMAL, bg=self.design.colors['success'])
            self.stop_btn.config(state=tk.DISABLED, bg=self.design.colors['bg_card'])
        else:
            self.fetch_btn.config(state=tk.DISABLED, bg=self.design.colors['text_muted'])
            self.stop_btn.config(state=tk.NORMAL, bg=self.design.colors['danger'], fg=self.design.colors['text_white'])
    
    def update_theme(self, design_system):
        """Update component colors when theme changes"""
        self.design = design_system
        
        # Update sidebar container
        self.parent.configure(bg=self.design.colors['bg_secondary'])
        
        # Update sidebar frame
        self.sidebar.configure(bg=self.design.colors['bg_sidebar'])
        
        # Update navigation buttons
        for btn, frame, is_active in self.nav_buttons:
            if is_active:
                btn.config(bg=self.design.colors['active'], fg=self.design.colors['primary'])
                frame.config(bg=self.design.colors['active'])
            else:
                btn.config(bg=self.design.colors['bg_sidebar'], fg=self.design.colors['text_primary'])
                frame.config(bg=self.design.colors['bg_sidebar'])
        
        # Update action buttons
        if hasattr(self, 'fetch_btn'):
            self.fetch_btn.config(bg=self.design.colors['success'])
        if hasattr(self, 'stop_btn'):
            self.stop_btn.config(bg=self.design.colors['bg_card'], fg=self.design.colors['danger'])
        
        # Update status section
        if hasattr(self, 'status_label'):
            self.status_label.config(fg=self.design.colors['text_secondary'], bg=self.design.colors['bg_primary'])
        if hasattr(self, 'status_dot'):
            self.status_dot.config(bg=self.design.colors['bg_primary'])

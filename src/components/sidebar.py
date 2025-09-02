"""
Sidebar Component Module
Contains the modern sidebar with navigation, actions, and status
"""

import tkinter as tk


class Sidebar:
    """Modern sidebar component with card design"""
    
    def __init__(self, parent, design_system, callbacks):
        self.parent = parent
        self.ds = design_system
        self.callbacks = callbacks
        self.nav_buttons = []
        self.create_sidebar()
    
    def create_sidebar(self):
        """Create modern sidebar with card design"""
        # Sidebar container
        sidebar_container = tk.Frame(
            self.parent,
            bg='red',  # Temporary color for visibility
            width=300,
            height=800
        )
        sidebar_container.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        sidebar_container.pack_propagate(False)
        
        # Sidebar card
        sidebar = tk.Frame(
            sidebar_container,
            bg='blue',  # Temporary color for visibility
            width=280,
            height=800
        )
        sidebar.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add a test label to verify visibility
        test_label = tk.Label(
            sidebar,
            text="SIDEBAR",
            font=('Arial', 24, 'bold'),
            bg='white',
            fg='black'
        )
        test_label.pack(expand=True)
        
        # Add navigation and other sections
        self.create_modern_navigation(sidebar)
        self.create_modern_actions(sidebar)
        self.create_sidebar_status(sidebar)
    
    def create_modern_search(self, parent):
        """Create modern search bar"""
        search_section = tk.Frame(
            parent, 
            bg=self.ds.colors['bg_sidebar']
        )
        search_section.pack(fill=tk.X, padx=self.ds.spacing['lg'], pady=self.ds.spacing['lg'])
        
        # Search container with pill shape
        search_container = tk.Frame(
            search_section,
            bg=self.ds.colors['bg_primary'],
            relief=tk.FLAT,
            bd=0
        )
        search_container.pack(fill=tk.X, ipady=self.ds.spacing['sm'])
        
        # Search icon
        search_icon = tk.Label(
            search_container,
            text="🔍",
            font=self.ds.fonts['body_medium'],
            bg=self.ds.colors['bg_primary'],
            fg=self.ds.colors['text_secondary']
        )
        search_icon.pack(side=tk.LEFT, padx=(self.ds.spacing['md'], self.ds.spacing['sm']))
        
        # Search entry
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_container,
            textvariable=self.search_var,
            font=self.ds.fonts['body_medium'],
            bg=self.ds.colors['bg_primary'],
            fg=self.ds.colors['text_primary'],
            border=0,
            relief=tk.FLAT
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, self.ds.spacing['md']))
        
        # Placeholder behavior
        search_entry.insert(0, "Search matches...")
        search_entry.bind('<FocusIn>', lambda e: self.on_search_focus_in(e))
        search_entry.bind('<FocusOut>', lambda e: self.on_search_focus_out(e))
    
    def create_modern_navigation(self, parent):
        """Create modern navigation menu"""
        nav_section = tk.Frame(parent, bg=self.ds.colors['bg_sidebar'])
        nav_section.pack(fill=tk.X, pady=self.ds.spacing['md'])
        
        # Navigation items with modern styling
        nav_items = [
            ("📊", "Live Matches", self.callbacks['show_live_matches'], True),
            ("📅", "Fixtures", self.callbacks['show_fixtures'], False),
            ("⭐", "Favorites", self.callbacks['show_favorites'], False),
            ("⚙️", "Settings", self.callbacks['show_settings'], False)
        ]
        
        self.nav_buttons = []
        for icon, text, command, active in nav_items:
            btn_frame = tk.Frame(nav_section, bg=self.ds.colors['bg_sidebar'])
            btn_frame.pack(fill=tk.X, padx=self.ds.spacing['md'], pady=self.ds.spacing['xs'])
            
            if active:
                btn_frame.config(bg=self.ds.colors['active'])
                
            btn = tk.Button(
                btn_frame,
                text=f"{icon}  {text}",
                font=self.ds.fonts['body_medium'],
                bg=self.ds.colors['active'] if active else self.ds.colors['bg_sidebar'],
                fg=self.ds.colors['primary'] if active else self.ds.colors['text_primary'],
                bd=0,
                relief=tk.FLAT,
                anchor='w',
                padx=self.ds.spacing['lg'],
                pady=self.ds.spacing['md'],
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
            bg=self.ds.colors['border'], 
            height=1
        )
        separator.pack(fill=tk.X, padx=self.ds.spacing['lg'], pady=self.ds.spacing['lg'])
    
    def create_modern_actions(self, parent):
        """Create modern action buttons"""
        action_section = tk.Frame(parent, bg=self.ds.colors['bg_sidebar'])
        action_section.pack(fill=tk.X, padx=self.ds.spacing['lg'], pady=self.ds.spacing['md'])
        
        # Fetch button with modern styling
        self.fetch_btn = tk.Button(
            action_section,
            text="🔄  Fetch Matches",
            font=self.ds.fonts['body_medium'],
            bg=self.ds.colors['success'],
            fg=self.ds.colors['text_white'],
            bd=0,
            relief=tk.FLAT,
            padx=self.ds.spacing['lg'],
            pady=self.ds.spacing['md'],
            command=self.callbacks['fetch_matches'],
            cursor='hand2'
        )
        self.fetch_btn.pack(fill=tk.X, pady=(0, self.ds.spacing['sm']))
        
        # Stop button
        self.stop_btn = tk.Button(
            action_section,
            text="⏹  Stop",
            font=self.ds.fonts['body_medium'],
            bg=self.ds.colors['bg_card'],
            fg=self.ds.colors['danger'],
            bd=1,
            relief=tk.SOLID,
            padx=self.ds.spacing['lg'],
            pady=self.ds.spacing['md'],
            command=self.callbacks['stop_fetching'],
            state=tk.DISABLED,
            cursor='hand2'
        )
        self.stop_btn.pack(fill=tk.X)
        
        # Button hover effects
        self.setup_button_hover_effects()
    
    def create_sidebar_status(self, parent):
        """Create sidebar status section"""
        status_section = tk.Frame(parent, bg=self.ds.colors['bg_sidebar'])
        status_section.pack(side=tk.BOTTOM, fill=tk.X, padx=self.ds.spacing['lg'], pady=self.ds.spacing['lg'])
        
        # Status indicator
        status_container = tk.Frame(
            status_section,
            bg=self.ds.colors['bg_primary'],
            relief=tk.FLAT
        )
        status_container.pack(fill=tk.X, pady=self.ds.spacing['sm'])
        
        # Status dot
        self.status_dot = tk.Label(
            status_container,
            text="●",
            font=self.ds.fonts['body_medium'],
            bg=self.ds.colors['bg_primary'],
            fg=self.ds.colors['success']
        )
        self.status_dot.pack(side=tk.LEFT, padx=(self.ds.spacing['md'], self.ds.spacing['sm']))
        
        # Status text
        self.status_label = tk.Label(
            status_container,
            text="Ready to fetch matches",
            font=self.ds.fonts['caption'],
            fg=self.ds.colors['text_secondary'],
            bg=self.ds.colors['bg_primary'],
            anchor='w'
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, self.ds.spacing['md']))
    
    def setup_button_hover_effects(self):
        """Setup hover effects for buttons"""
        def fetch_hover_enter(e):
            self.fetch_btn.config(bg=self.ds.colors['text_primary'])
        
        def fetch_hover_leave(e):
            if self.fetch_btn['state'] != tk.DISABLED:
                self.fetch_btn.config(bg=self.ds.colors['success'])
        
        def stop_hover_enter(e):
            if self.stop_btn['state'] != tk.DISABLED:
                self.stop_btn.config(bg=self.ds.colors['text_primary'])
        
        def stop_hover_leave(e):
            if self.stop_btn['state'] != tk.DISABLED:
                self.stop_btn.config(bg=self.ds.colors['danger'])
        
        self.fetch_btn.bind('<Enter>', fetch_hover_enter)
        self.fetch_btn.bind('<Leave>', fetch_hover_leave)
        self.stop_btn.bind('<Enter>', stop_hover_enter)
        self.stop_btn.bind('<Leave>', stop_hover_leave)
    
    def nav_hover_enter(self, button, frame):
        """Navigation hover enter effect"""
        if button.cget('bg') != self.ds.colors['active']:
            button.config(bg=self.ds.colors['hover'])
            frame.config(bg=self.ds.colors['hover'])
    
    def nav_hover_leave(self, button, frame, is_active):
        """Navigation hover leave effect"""
        if is_active:
            button.config(bg=self.ds.colors['active'])
            frame.config(bg=self.ds.colors['active'])
        else:
            button.config(bg=self.ds.colors['bg_sidebar'])
            frame.config(bg=self.ds.colors['bg_sidebar'])
    
    def on_search_focus_in(self, event):
        """Handle search focus in"""
        if event.widget.get() == "Search matches...":
            event.widget.delete(0, tk.END)
            event.widget.config(fg=self.ds.colors['text_primary'])
    
    def on_search_focus_out(self, event):
        """Handle search focus out"""
        if not event.widget.get():
            event.widget.insert(0, "Search matches...")
            event.widget.config(fg=self.ds.colors['text_muted'])
    
    def update_nav_selection(self, active_index):
        """Update navigation selection styling"""
        for i, (btn, frame, _) in enumerate(self.nav_buttons):
            if i == active_index:
                btn.config(bg=self.ds.colors['active'], fg=self.ds.colors['primary'])
                frame.config(bg=self.ds.colors['active'])
                self.nav_buttons[i] = (btn, frame, True)
            else:
                btn.config(bg=self.ds.colors['bg_sidebar'], fg=self.ds.colors['text_primary'])
                frame.config(bg=self.ds.colors['bg_sidebar'])
                self.nav_buttons[i] = (btn, frame, False)
    
    def update_status(self, message, color, indicator="●"):
        """Update status with modern styling"""
        self.status_label.config(text=message, fg=color)
        self.status_dot.config(fg=color, text=indicator)
    
    def set_fetch_button_state(self, enabled):
        """Set fetch button state"""
        if enabled:
            self.fetch_btn.config(state=tk.NORMAL, bg=self.ds.colors['success'])
        else:
            self.fetch_btn.config(state=tk.DISABLED, bg=self.ds.colors['text_muted'])
    
    def set_stop_button_state(self, enabled):
        """Set stop button state"""
        if enabled:
            self.stop_btn.config(state=tk.NORMAL, bg=self.ds.colors['danger'], fg=self.ds.colors['text_white'])
        else:
            self.stop_btn.config(state=tk.DISABLED, bg=self.ds.colors['bg_card'], fg=self.ds.colors['danger'])

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
        self.sidebar_container = tk.Frame(
            self.parent,
            bg=self.design.colors['bg_secondary'],
            width=300,
            height=800
        )
        self.sidebar_container.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        self.sidebar_container.pack_propagate(False)
        
        # Store references to themed widgets
        self.themed_widgets = []
        
        # Sidebar card
        self.sidebar = tk.Frame(
            self.sidebar_container,
            bg=self.design.colors['bg_sidebar'],
            width=280,
            height=800
        )
        self.sidebar.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.themed_widgets.extend([self.sidebar_container, self.sidebar])
        
        # Add navigation and other sections
        self.create_modern_search()
        self.create_modern_navigation()
        self.create_modern_actions()
        self.create_sidebar_status()
    
    def create_modern_search(self):
        """Create a modern search bar with enhanced styling and functionality"""
        # Search section with proper spacing
        self.search_section = tk.Frame(
            self.sidebar, 
            bg=self.design.colors['bg_sidebar']
        )
        self.search_section.pack(fill=tk.X, padx=self.design.spacing['md'], pady=(self.design.spacing['lg'], self.design.spacing['md']))
        self.themed_widgets.append(self.search_section)
        
        # Search container with modern styling
        search_bg = self.design.colors['bg_secondary'] if self.design.is_dark_theme() else '#F5F5F5'
        self.search_container = tk.Frame(
            self.search_section,
            bg=search_bg,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=self.design.colors['border'],
            highlightcolor=self.design.colors['primary']
        )
        self.search_container.pack(fill=tk.X, ipady=8, ipadx=12)
        self.search_container.bind('<Enter>', lambda e: self.on_search_hover(True))
        self.search_container.bind('<Leave>', lambda e: self.on_search_hover(False))
        self.themed_widgets.append(self.search_container)
        
        # Search icon with modern styling
        self.search_icon = tk.Label(
            self.search_container,
            text="\U0001F50D",  # Magnifying glass emoji
            font=('Segoe UI Emoji', 14),
            bg=search_bg,
            fg=self.design.colors['text_secondary']
        )
        self.search_icon.pack(side=tk.LEFT, padx=(4, 8))
        self.themed_widgets.append(self.search_icon)
        
        # Search entry with modern styling
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            self.search_container,
            textvariable=self.search_var,
            font=('Segoe UI', 12),
            bg=search_bg,
            fg=self.design.colors['text_primary'],
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            insertbackground=self.design.colors['text_primary'],
            selectbackground=self.design.colors['primary'],
            selectforeground='white'
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.themed_widgets.append(self.search_entry)
        
        # Clear button (initially hidden)
        self.clear_button = tk.Label(
            self.search_container,
            text="✕",
            font=('Segoe UI', 12, 'bold'),
            bg=search_bg,
            fg=self.design.colors['text_secondary'],
            cursor='hand2'
        )
        self.clear_button.pack(side=tk.RIGHT, padx=(0, 4))
        self.clear_button.bind('<Button-1>', self.clear_search)
        self.clear_button.pack_forget()  # Initially hidden
        self.themed_widgets.append(self.clear_button)
        
        # Placeholder behavior and search functionality
        self.search_entry.insert(0, "Search matches...")
        self.search_entry.config(fg=self.design.colors['text_secondary'])
        self.search_entry.bind('<FocusIn>', self.on_search_focus_in)
        self.search_entry.bind('<FocusOut>', self.on_search_focus_out)
        self.search_var.trace('w', self.on_search_typing)
        self.search_entry.bind('<Return>', self.perform_search)
    
    def create_modern_navigation(self):
        """Create modern navigation section"""
        self.nav_section = tk.Frame(
            self.sidebar,
            bg=self.design.colors['bg_sidebar']
        )
        self.nav_section.pack(fill=tk.X, pady=(0, self.design.spacing['xl']))
        self.themed_widgets.append(self.nav_section)
        
        # Navigation items with modern styling
        nav_items = [
            ("📊", "Live Matches", self.callbacks['show_live_matches'], True),
            ("📅", "Fixtures", self.callbacks['show_fixtures'], False),
            ("🏁", "Finished", self.callbacks['show_finished'], False),
            ("⚙️", "Settings", self.callbacks['show_settings'], False)
        ]
        
        self.nav_buttons = []
        for icon, text, command, is_active in nav_items:
            btn_frame = tk.Frame(self.nav_section, bg=self.design.colors['bg_sidebar'])
            btn_frame.pack(fill=tk.X, pady=(0, self.design.spacing['xs']))
            self.themed_widgets.append(btn_frame)
            
            btn = tk.Label(
                btn_frame,
                text=f"{icon}  {text}",
                font=self.design.fonts['body_medium'],
                bg=self.design.colors['bg_sidebar'],
                fg=self.design.colors['text_primary'] if is_active else self.design.colors['text_secondary'],
                anchor='w',
                padx=self.design.spacing['lg'],
                pady=self.design.spacing['md'],
                cursor='hand2'
            )
            btn.pack(fill=tk.X)
            self.themed_widgets.append(btn)
            
            # Add hover effect
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.design.colors['hover']))
            btn.bind('<Leave>', lambda e, b=btn, active=is_active: 
                    b.config(bg=self.design.colors['bg_sidebar'],
                            fg=self.design.colors['text_primary'] if active else self.design.colors['text_secondary']))
            
            # Add click handler
            btn.bind('<Button-1>', lambda e, cmd=command: self.on_nav_click(cmd, btn_frame))
            
            self.nav_buttons.append((btn_frame, btn))
        
        # Separator
        separator = tk.Frame(
            self.nav_section, 
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
            bg=self.design.colors['bg_secondary'],
            relief=tk.FLAT
        )
        status_container.pack(fill=tk.X, pady=self.design.spacing['sm'])
        
        # Status dot
        self.status_dot = tk.Label(
            status_container,
            text="●",
            font=self.design.fonts['body_medium'],
            bg=self.design.colors['bg_secondary'],
            fg=self.design.colors['success']
        )
        self.status_dot.pack(side=tk.LEFT, padx=(self.design.spacing['md'], self.design.spacing['sm']))
        
        # Status text
        self.status_label = tk.Label(
            status_container,
            text="Ready to fetch matches",
            font=self.design.fonts['caption'],
            fg=self.design.colors['text_secondary'],
            bg=self.design.colors['bg_secondary'],
            anchor='w'
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, self.design.spacing['md']))
    
    def refresh(self):
        """Refresh the sidebar after theme changes"""
        try:
            # Save current status before refresh
            status_text = self.status_label.cget('text') if hasattr(self, 'status_label') else ""
            status_color = self.status_dot.cget('fg') if hasattr(self, 'status_dot') else ""
            status_emoji = self.status_dot.cget('text') if hasattr(self, 'status_dot') else ""
            
            # Clear existing widgets
            for widget in self.sidebar_container.winfo_children():
                widget.destroy()
            
            # Clear the container's grid/pack settings
            self.sidebar_container.pack_forget()
            
            # Recreate the sidebar with updated theme
            self.create_sidebar()
            
            # Repack the sidebar container with proper settings
            self.sidebar_container.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
            
            # Update status if it existed before
            if hasattr(self, 'update_status') and status_text:
                self.update_status(status_text, status_color, status_emoji)
                
        except Exception as e:
            print(f"Error refreshing sidebar: {e}")
    
    def update_theme(self, design_system):
        """Update theme colors for all widgets"""
        self.design = design_system
        
        try:
            # Update main containers
            if hasattr(self, 'sidebar_container'):
                self.sidebar_container.config(bg=self.design.colors['bg_secondary'])
            if hasattr(self, 'sidebar'):
                self.sidebar.config(bg=self.design.colors['bg_sidebar'])
            
            # Update all themed widgets
            if hasattr(self, 'themed_widgets'):
                for widget in self.themed_widgets:
                    try:
                        if isinstance(widget, tk.Frame):
                            if hasattr(self, 'search_container') and widget == self.search_container:
                                widget.config(bg=self.design.colors['bg_secondary'])
                            else:
                                widget.config(bg=self.design.colors['bg_sidebar'])
                        elif isinstance(widget, tk.Label):
                            if hasattr(self, 'search_icon') and widget == self.search_icon:
                                widget.config(
                                    bg=self.design.colors['bg_secondary'], 
                                    fg=self.design.colors['text_secondary']
                                )
                            else:
                                widget.config(
                                    bg=self.design.colors['bg_sidebar'], 
                                    fg=self.design.colors['text_primary']
                                )
                        elif isinstance(widget, tk.Entry):
                            widget.config(
                                bg=self.design.colors['bg_secondary'],
                                fg=self.design.colors['text_primary'],
                                insertbackground=self.design.colors['text_primary']
                            )
                    except Exception as e:
                        print(f"Error updating widget theme: {e}")
            
            # Update buttons if they exist
            if hasattr(self, 'fetch_btn'):
                self.fetch_btn.config(
                    bg=self.design.colors['success'], 
                    fg=self.design.colors['text_white'],
                    activebackground=self.design.colors['success'],
                    activeforeground=self.design.colors['text_white']
                )
            
            if hasattr(self, 'stop_btn'):
                self.stop_btn.config(
                    bg=self.design.colors['bg_card'], 
                    fg=self.design.colors['danger'],
                    activebackground=self.design.colors['bg_card'],
                    activeforeground=self.design.colors['danger']
                )
            
            # Update status section if it exists
            if hasattr(self, 'status_frame'):
                self.status_frame.config(bg=self.design.colors['bg_sidebar'])
            
            if hasattr(self, 'status_dot'):
                self.status_dot.config(
                    bg=self.design.colors['bg_sidebar'], 
                    fg=self.design.colors['success']
                )
            
            if hasattr(self, 'status_label'):
                self.status_label.config(
                    bg=self.design.colors['bg_sidebar'], 
                    fg=self.design.colors['text_secondary']
                )
                
        except Exception as e:
            print(f"Error in sidebar theme update: {e}")
        
        # Update button styles
        self.setup_button_hover_effects()
        
        # Refresh the sidebar to apply all theme changes
        self.refresh()
    
    def on_nav_click(self, command, btn_frame):
        """Handle navigation button click"""
        # Update button states
        for frame, btn in self.nav_buttons:
            btn.config(fg=self.design.colors['text_secondary'])
            
        # Highlight the selected button
        for frame, btn in self.nav_buttons:
            if frame == btn_frame:
                btn.config(fg=self.design.colors['text_primary'])
        
        # Execute the command
        command()
    
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
    
    def on_search_hover(self, is_hover):
        """Handle search bar hover effects"""
        if is_hover:
            self.search_container.config(highlightbackground=self.design.colors['primary'])
        else:
            self.search_container.config(highlightbackground=self.design.colors['border'])
    
    def on_search_focus_in(self, event):
        """Handle search focus in with enhanced styling"""
        current_text = event.widget.get()
        if current_text == "Search matches...":
            event.widget.delete(0, tk.END)
            event.widget.config(fg=self.design.colors['text_primary'])
        
        # Show clear button if there's text
        if hasattr(self, 'clear_button') and current_text and current_text != "Search matches...":
            self.clear_button.pack(side=tk.RIGHT, padx=(0, 4))
        
        # Update border color on focus
        self.search_container.config(highlightbackground=self.design.colors['primary'])
    
    def on_search_focus_out(self, event):
        """Handle search focus out with enhanced styling"""
        current_text = event.widget.get()
        if not current_text:
            event.widget.insert(0, "Search matches...")
            event.widget.config(fg=self.design.colors['text_secondary'])
        
        # Hide clear button if no text
        if hasattr(self, 'clear_button') and (not current_text or current_text == "Search matches..."):
            self.clear_button.pack_forget()
        
        # Reset border color
        self.search_container.config(highlightbackground=self.design.colors['border'])
    
    def on_search_typing(self, *args):
        """Handle search text changes"""
        search_text = self.search_var.get()
        if search_text and search_text != "Search matches...":
            if not self.clear_button.winfo_ismapped():
                self.clear_button.pack(side=tk.RIGHT, padx=(0, 4))
        else:
            self.clear_button.pack_forget()
    
    def clear_search(self, event=None):
        """Clear the search field"""
        self.search_var.set("")
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, "Search matches...")
        self.search_entry.config(fg=self.design.colors['text_secondary'])
        self.clear_button.pack_forget()
        self.search_entry.focus()
        # You can add search clearing logic here
        
    def perform_search(self, event=None):
        """Perform the search operation"""
        search_text = self.search_var.get()
        if search_text and search_text != "Search matches...":
            # Add your search logic here
            print(f"Searching for: {search_text}")
            # Example: self.callbacks.get('search_matches')(search_text)
    
    def update_nav_selection(self, index):
        """Update the selected navigation item"""
        if not hasattr(self, 'nav_buttons'):
            return
            
        for i, (frame, btn) in enumerate(self.nav_buttons):
            try:
                if i == index:
                    btn.config(
                        fg=self.design.colors['text_primary'],
                        bg=self.design.colors['hover']
                    )
                    frame.config(bg=self.design.colors['hover'])
                else:
                    btn.config(
                        fg=self.design.colors['text_secondary'],
                        bg=self.design.colors['bg_sidebar']
                    )
                    frame.config(bg=self.design.colors['bg_sidebar'])
            except Exception as e:
                print(f"Error updating nav selection: {e}")
    
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
        
        # Update search section
        if hasattr(self, 'search_entry'):
            search_bg = self.design.colors['bg_secondary'] if self.design.is_dark_theme() else '#F1F3F4'
            self.search_entry.config(
                bg=search_bg,
                fg=self.design.colors['text_primary']
            )
        
        # Update search container
        for widget in self.sidebar.winfo_children():
            if isinstance(widget, tk.Frame):
                self.update_search_containers(widget)
        
        # Update status section
        if hasattr(self, 'status_label'):
            status_bg = self.design.colors['bg_secondary'] if self.design.is_dark_theme() else '#F1F3F4'
            self.status_label.config(fg=self.design.colors['text_secondary'], bg=status_bg)
        if hasattr(self, 'status_dot'):
            status_bg = self.design.colors['bg_secondary'] if self.design.is_dark_theme() else '#F1F3F4'
            self.status_dot.config(bg=status_bg)
        
        # Update status container
        for widget in self.sidebar.winfo_children():
            if isinstance(widget, tk.Frame):
                self.update_status_containers(widget)
    
    def update_search_containers(self, widget):
        """Update search container themes"""
        if isinstance(widget, tk.Frame):
            # Check if this is a search container by looking for search entry
            for child in widget.winfo_children():
                if isinstance(child, tk.Entry) and hasattr(self, 'search_entry') and child == self.search_entry:
                    search_bg = self.design.colors['bg_secondary'] if self.design.is_dark_theme() else '#F1F3F4'
                    widget.configure(bg=search_bg)
                    # Update search icon
                    for grandchild in widget.winfo_children():
                        if isinstance(grandchild, tk.Label) and grandchild.cget('text') == "🔍":
                            grandchild.config(
                                bg=search_bg,
                                fg=self.design.colors['text_secondary']
                            )
                else:
                    self.update_search_containers(child)
    
    def update_status_containers(self, widget):
        """Update status container themes"""
        if isinstance(widget, tk.Frame):
            # Check if this is a status container by looking for status elements
            for child in widget.winfo_children():
                if isinstance(child, tk.Label) and hasattr(self, 'status_label') and child == self.status_label:
                    status_bg = self.design.colors['bg_secondary'] if self.design.is_dark_theme() else '#F1F3F4'
                    widget.configure(bg=status_bg)
                elif isinstance(child, tk.Label) and hasattr(self, 'status_dot') and child == self.status_dot:
                    status_bg = self.design.colors['bg_secondary'] if self.design.is_dark_theme() else '#F1F3F4'
                    widget.configure(bg=status_bg)
                else:
                    self.update_status_containers(child)

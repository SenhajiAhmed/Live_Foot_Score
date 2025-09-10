"""
Content Area Component Module
Contains the main content area with match display and scrolling functionality.
"""

import tkinter as tk
from tkinter import ttk


class ContentArea:
    """Modern content area component with match display and scrolling."""
    
    def __init__(self, parent, design_system):
        self.parent = parent
        self.design = design_system
        self.current_view = "live_matches"
        self.match_display = None  # Will be set by main app
        self.match_organizer = None  # Will be set by main app
        
        self.create_content_area()
        self.setup_modern_scrollable_area()
        self.show_modern_empty_state()
    
    def create_content_area(self):
        """Create modern content area"""
        self.content = tk.Frame(
            self.parent, 
            bg=self.design.colors['bg_card'],
            relief=tk.FLAT,
            bd=1,
            highlightbackground=self.design.colors['border'],
            highlightthickness=1
        )
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Content header
        header = tk.Frame(self.content, bg=self.design.colors['bg_card'], height=80)
        header.pack(fill=tk.X, padx=self.design.spacing['xl'], pady=self.design.spacing['lg'])
        header.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header, bg=self.design.colors['bg_card'])
        header_content.pack(expand=True)
        
        self.content_title = tk.Label(
            header_content,
            text="Live Matches",
            font=self.design.fonts['display_medium'],
            fg=self.design.colors['text_primary'],
            bg=self.design.colors['bg_card'],
            anchor='w'
        )
        self.content_title.pack(fill=tk.X)
        
        # Subtitle
        self.content_subtitle = tk.Label(
            header_content,
            text="Real-time football scores and updates",
            font=self.design.fonts['body_medium'],
            fg=self.design.colors['text_secondary'],
            bg=self.design.colors['bg_card'],
            anchor='w'
        )
        self.content_subtitle.pack(fill=tk.X, pady=(self.design.spacing['xs'], 0))
        
        # Matches container with modern scrolling
        self.matches_container = tk.Frame(self.content, bg=self.design.colors['bg_card'])
        self.matches_container.pack(fill=tk.BOTH, expand=True, padx=self.design.spacing['xl'], pady=(0, self.design.spacing['lg']))
    
    def setup_modern_scrollable_area(self):
        """Setup modern scrollable area with custom styling"""
        # Canvas for scrolling
        self.canvas = tk.Canvas(
            self.matches_container,
            bg=self.design.colors['bg_card'],
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
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.design.colors['bg_card'])
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
        
        # Setup virtual scrolling for better performance
        if hasattr(self.match_display, 'setup_virtual_scrolling'):
            self.match_display.setup_virtual_scrolling(self.canvas)
    
    def show_modern_empty_state(self, message="No matches available", subtitle="Click 'Fetch Matches' to get the latest scores"):
        """Show modern empty state"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        empty_container = tk.Frame(self.scrollable_frame, bg=self.design.colors['bg_card'])
        empty_container.pack(expand=True, fill=tk.BOTH)
        
        # Center the empty state
        empty_frame = tk.Frame(empty_container, bg=self.design.colors['bg_card'])
        empty_frame.pack(expand=True)
        
        # Large icon
        tk.Label(
            empty_frame,
            text="⚽",
            font=('Inter', 64),
            fg=self.design.colors['text_muted'],
            bg=self.design.colors['bg_card']
        ).pack(pady=(0, self.design.spacing['lg']))
        
        # Main message
        tk.Label(
            empty_frame,
            text=message,
            font=self.design.fonts['headline'],
            fg=self.design.colors['text_secondary'],
            bg=self.design.colors['bg_card']
        ).pack(pady=(0, self.design.spacing['sm']))
        
        # Subtitle
        tk.Label(
            empty_frame,
            text=subtitle,
            font=self.design.fonts['body_medium'],
            fg=self.design.colors['text_muted'],
            bg=self.design.colors['bg_card']
        ).pack()
    
    def show_modern_loading_state(self):
        """Show modern loading state with skeleton screens"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        loading_frame = tk.Frame(self.scrollable_frame, bg=self.design.colors['bg_card'])
        loading_frame.pack(fill=tk.BOTH, expand=True, padx=self.design.spacing['lg'], pady=self.design.spacing['lg'])
        
        # Create skeleton cards
        for i in range(3):
            self.create_skeleton_card(loading_frame)
    
    def create_skeleton_card(self, parent):
        """Create skeleton loading card"""
        skeleton_card = tk.Frame(
            parent,
            bg=self.design.colors['bg_primary'],
            relief=tk.FLAT,
            bd=1,
            highlightbackground=self.design.colors['border'],
            highlightthickness=1
        )
        skeleton_card.pack(fill=tk.X, pady=self.design.spacing['sm'])
        
        # Skeleton content
        content = tk.Frame(skeleton_card, bg=self.design.colors['bg_primary'])
        content.pack(fill=tk.X, padx=self.design.spacing['lg'], pady=self.design.spacing['lg'])
        
        # Tournament name skeleton
        tk.Frame(
            content,
            bg=self.design.colors['border'],
            height=20,
            width=200
        ).pack(anchor='w', pady=(0, self.design.spacing['md']))
        
        # Match skeleton
        match_frame = tk.Frame(content, bg=self.design.colors['bg_primary'])
        match_frame.pack(fill=tk.X)
        
        for _ in range(2):
            tk.Frame(
                match_frame,
                bg=self.design.colors['border'],
                height=15,
                width=150
            ).pack(anchor='w', pady=self.design.spacing['xs'])
    
    def smooth_scroll(self, event):
        """Smooth scrolling for canvas"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def update_content_title(self, title, subtitle):
        """Update content title and subtitle"""
        self.content_title.config(text=title)
        self.content_subtitle.config(text=subtitle)
    
    def clear_content(self):
        """Clear all content from the scrollable area"""
        # Stop any ongoing rendering
        if self.match_display and hasattr(self.match_display, 'stop_rendering'):
            self.match_display.stop_rendering()
        
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
    
    def set_match_display(self, match_display):
        """Set the match display component"""
        self.match_display = match_display
    
    def set_match_organizer(self, match_organizer):
        """Set the match organizer component"""
        self.match_organizer = match_organizer
    
    def show_live_matches(self, data=None):
        """Show live matches view"""
        self.current_view = "live_matches"
        self.update_content_title("Live Matches", "Real-time football scores and updates")
        
        if data:
            filtered_data = self.filter_live_matches(data)
            if filtered_data:
                self.display_matches(filtered_data)
            else:
                self.show_modern_empty_state("No live matches", "No matches are currently in progress")
        else:
            self.show_modern_empty_state("No live matches", "Click 'Fetch Matches' to get the latest scores")
    
    def show_fixtures(self, data=None):
        """Show upcoming fixtures view"""
        self.current_view = "fixtures"
        self.update_content_title("Upcoming Fixtures", "Scheduled matches and kick-off times")
        
        if data:
            filtered_data = self.filter_upcoming_matches(data)
            if filtered_data:
                self.display_matches(filtered_data)
            else:
                self.show_modern_empty_state("No upcoming matches", "No fixtures scheduled at the moment")
        else:
            self.show_modern_empty_state("No upcoming matches", "Click 'Fetch Matches' to get the latest fixtures")
    
    def show_finished(self, data=None):
        """Show finished matches view"""
        self.current_view = "finished"
        self.update_content_title("Finished Matches", "Completed matches and final scores")
        
        if data:
            filtered_data = self.filter_finished_matches(data)
            if filtered_data:
                self.display_matches(filtered_data)
            else:
                self.show_modern_empty_state("No finished matches", "No completed matches available at the moment")
        else:
            self.show_modern_empty_state("No finished matches", "Click 'Fetch Matches' to get the latest results")
    
    def show_settings(self):
        """Show settings view"""
        self.current_view = "settings"
        self.update_content_title("Settings", "Customize your experience")
        self.show_settings_content()
    
    def filter_live_matches(self, data):
        """Filter data to show only live matches"""
        if not data or 'events' not in data:
            return None
        
        live_events = []
        for event in data['events']:
            if event['status']['type'] == 'inprogress':
                live_events.append(event)
        
        if live_events:
            return {'events': live_events}
        return None
    
    def filter_upcoming_matches(self, data):
        """Filter data to show only upcoming matches"""
        if not data or 'events' not in data:
            return None
        
        upcoming_events = []
        for event in data['events']:
            if event['status']['type'] not in ['inprogress', 'finished']:
                upcoming_events.append(event)
        
        if upcoming_events:
            return {'events': upcoming_events}
        return None
    
    def filter_finished_matches(self, data):
        """Filter data to show only finished matches"""
        if not data or 'events' not in data:
            return None
        
        finished_events = []
        for event in data['events']:
            if event['status']['type'] == 'finished':
                finished_events.append(event)
        
        if finished_events:
            return {'events': finished_events}
        return None
    
    def display_matches(self, data):
        """Display matches using the match display component with lazy loading"""
        if not self.match_display:
            self.show_modern_empty_state("Error", "Match display component not initialized")
            return
        
        # Clear previous content
        self.clear_content()
        
        # Organize matches by tournament
        if not self.match_organizer:
            self.show_modern_empty_state("Error", "Match organizer not initialized")
            return
            
        matches_by_tournament = self.match_organizer.organize_matches_by_tournament(data)
        
        if matches_by_tournament:
            # Start lazy loading directly without showing loading state
            total_matches = self.match_display.display_tournaments(
                self.scrollable_frame, 
                matches_by_tournament
            )
            print(f"Starting lazy loading of {total_matches} matches in {self.current_view} view")
            
            # Add load more button if there are more matches available
            if data.get('total_available', 0) > data.get('showing', 0):
                self.add_load_more_button(data)
        else:
            self.show_modern_empty_state("No matches found", "Try refreshing the data")
    
    
    def add_load_more_button(self, data):
        """Add a load more button for additional matches"""
        load_more_frame = tk.Frame(self.scrollable_frame, bg=self.design.colors['bg_card'])
        load_more_frame.pack(fill=tk.X, padx=self.design.spacing['xl'], pady=self.design.spacing['lg'])
        
        # Load more button
        load_more_btn = tk.Button(
            load_more_frame,
            text=f"Load More Matches ({data.get('total_available', 0) - data.get('showing', 0)} remaining)",
            font=self.design.fonts['body_medium'],
            bg=self.design.colors['primary'],
            fg=self.design.colors['text_white'],
            bd=0,
            relief=tk.FLAT,
            padx=self.design.spacing['lg'],
            pady=self.design.spacing['md'],
            cursor='hand2',
            command=lambda: self.load_more_matches(data)
        )
        load_more_btn.pack()
        
        # Add hover effect
        def on_enter(e):
            load_more_btn.config(bg=self.design.colors.get('primary_hover', self.design.colors['primary']))
        
        def on_leave(e):
            load_more_btn.config(bg=self.design.colors['primary'])
        
        load_more_btn.bind('<Enter>', on_enter)
        load_more_btn.bind('<Leave>', on_leave)
    
    def load_more_matches(self, data):
        """Load more matches when button is clicked"""
        # This would be implemented to load additional matches
        # For now, just show a message
        print("Load more matches functionality would be implemented here")
    
    def show_settings_content(self):
        """Show settings content"""
        self.clear_content()
        
        settings_container = tk.Frame(self.scrollable_frame, bg=self.design.colors['bg_card'])
        settings_container.pack(fill=tk.BOTH, expand=True, padx=self.design.spacing['xl'], pady=self.design.spacing['xl'])
        
        # Settings title
        title_frame = tk.Frame(settings_container, bg=self.design.colors['bg_card'])
        title_frame.pack(fill=tk.X, pady=(0, self.design.spacing['lg']))
        
        tk.Label(
            title_frame,
            text="⚙️ Application Settings",
            font=self.design.fonts['headline'],
            fg=self.design.colors['text_primary'],
            bg=self.design.colors['bg_card'],
            anchor='w'
        ).pack(fill=tk.X)
        
        # Theme toggle section
        self.create_theme_toggle_section(settings_container)
        
        # Settings sections
        self.create_settings_section(settings_container, "Display", [
            ("Auto-refresh", "Automatically refresh match data"),
            ("Show notifications", "Show desktop notifications")
        ])
        
        self.create_settings_section(settings_container, "Data", [
            ("Cache duration", "How long to cache match data"),
            ("Update frequency", "How often to check for updates"),
            ("Save favorites", "Remember favorite matches")
        ])
        
        self.create_settings_section(settings_container, "About", [
            ("Version", "Football Scores Pro v1.0"),
            ("Developer", "Built with Python & Tkinter"),
            ("Data source", "Live football data API")
        ])
    
    def create_settings_section(self, parent, section_title, options):
        """Create a settings section"""
        section_frame = tk.Frame(parent, bg=self.design.colors['bg_card'])
        section_frame.pack(fill=tk.X, pady=(0, self.design.spacing['lg']))
        
        # Section title
        tk.Label(
            section_frame,
            text=section_title,
            font=self.design.fonts['body_large'],
            fg=self.design.colors['primary'],
            bg=self.design.colors['bg_card'],
            anchor='w'
        ).pack(fill=tk.X, pady=(0, self.design.spacing['md']))
        
        # Options
        for option, description in options:
            option_frame = tk.Frame(section_frame, bg=self.design.colors['bg_card'])
            option_frame.pack(fill=tk.X, pady=self.design.spacing['xs'])
            
            # Option name
            tk.Label(
                option_frame,
                text=option,
                font=self.design.fonts['body_medium'],
                fg=self.design.colors['text_primary'],
                bg=self.design.colors['bg_card'],
                anchor='w'
            ).pack(side=tk.LEFT)
            
            # Option description
            tk.Label(
                option_frame,
                text=description,
                font=self.design.fonts['caption'],
                fg=self.design.colors['text_secondary'],
                bg=self.design.colors['bg_card'],
                anchor='w'
            ).pack(side=tk.LEFT, padx=(self.design.spacing['md'], 0))
    
    def create_theme_toggle_section(self, parent):
        """Create interactive theme toggle section"""
        theme_frame = tk.Frame(parent, bg=self.design.colors['bg_card'])
        theme_frame.pack(fill=tk.X, pady=(0, self.design.spacing['lg']))
        
        # Section title
        tk.Label(
            theme_frame,
            text="Theme",
            font=self.design.fonts['body_large'],
            fg=self.design.colors['primary'],
            bg=self.design.colors['bg_card'],
            anchor='w'
        ).pack(fill=tk.X, pady=(0, self.design.spacing['md']))
        
        # Theme toggle container
        toggle_container = tk.Frame(theme_frame, bg=self.design.colors['bg_card'])
        toggle_container.pack(fill=tk.X)
        
        # Current theme label
        self.theme_status_label = tk.Label(
            toggle_container,
            text=f"Current: {self.design.get_theme().title()} Mode",
            font=self.design.fonts['body_medium'],
            fg=self.design.colors['text_primary'],
            bg=self.design.colors['bg_card'],
            anchor='w'
        )
        self.theme_status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Theme toggle buttons
        button_frame = tk.Frame(toggle_container, bg=self.design.colors['bg_card'])
        button_frame.pack(side=tk.RIGHT)
        
        # Light mode button
        self.light_btn = tk.Button(
            button_frame,
            text="☀️ Light",
            font=self.design.fonts['body_medium'],
            bg=self.design.colors['primary'] if not self.design.is_dark_theme() else self.design.colors['bg_card'],
            fg=self.design.colors['text_white'] if not self.design.is_dark_theme() else self.design.colors['text_primary'],
            bd=1,
            relief=tk.SOLID if self.design.is_dark_theme() else tk.FLAT,
            padx=self.design.spacing['md'],
            pady=self.design.spacing['sm'],
            command=lambda: self.toggle_theme('light'),
            cursor='hand2'
        )
        self.light_btn.pack(side=tk.LEFT, padx=(0, self.design.spacing['sm']))
        
        # Dark mode button
        self.dark_btn = tk.Button(
            button_frame,
            text="🌙 Dark",
            font=self.design.fonts['body_medium'],
            bg=self.design.colors['primary'] if self.design.is_dark_theme() else self.design.colors['bg_card'],
            fg=self.design.colors['text_white'] if self.design.is_dark_theme() else self.design.colors['text_primary'],
            bd=1,
            relief=tk.SOLID if not self.design.is_dark_theme() else tk.FLAT,
            padx=self.design.spacing['md'],
            pady=self.design.spacing['sm'],
            command=lambda: self.toggle_theme('dark'),
            cursor='hand2'
        )
        self.dark_btn.pack(side=tk.LEFT)
    
    def toggle_theme(self, theme):
        """Toggle between light and dark themes"""
        if hasattr(self, 'theme_callback') and self.theme_callback:
            self.theme_callback(theme)
        else:
            # Fallback: update design system directly
            self.design.switch_theme(theme)
            self.update_theme_buttons()
    
    def set_theme_callback(self, callback):
        """Set callback function for theme changes"""
        self.theme_callback = callback
    
    def update_theme_buttons(self):
        """Update theme toggle buttons appearance"""
        if hasattr(self, 'theme_status_label'):
            self.theme_status_label.config(text=f"Current: {self.design.get_theme().title()} Mode")
        
        if hasattr(self, 'light_btn') and hasattr(self, 'dark_btn'):
            # Update light button
            self.light_btn.config(
                bg=self.design.colors['primary'] if not self.design.is_dark_theme() else self.design.colors['bg_card'],
                fg=self.design.colors['text_white'] if not self.design.is_dark_theme() else self.design.colors['text_primary'],
                relief=tk.FLAT if not self.design.is_dark_theme() else tk.SOLID
            )
            
            # Update dark button
            self.dark_btn.config(
                bg=self.design.colors['primary'] if self.design.is_dark_theme() else self.design.colors['bg_card'],
                fg=self.design.colors['text_white'] if self.design.is_dark_theme() else self.design.colors['text_primary'],
                relief=tk.FLAT if self.design.is_dark_theme() else tk.SOLID
            )
    
    def update_theme(self, design_system=None):
        """Update component colors when theme changes"""
        if design_system:
            self.design = design_system
        
        try:
            # Update content frame
            if hasattr(self, 'content'):
                self.content.configure(bg=self.design.colors['bg_card'])
            
            # Update content title and subtitle
            if hasattr(self, 'content_title'):
                self.content_title.config(
                    fg=self.design.colors['text_primary'], 
                    bg=self.design.colors['bg_card']
                )
            
            if hasattr(self, 'content_subtitle'):
                self.content_subtitle.config(
                    fg=self.design.colors['text_secondary'], 
                    bg=self.design.colors['bg_card']
                )
            
            # Update canvas and scrollable frame
            if hasattr(self, 'canvas'):
                self.canvas.configure(bg=self.design.colors['bg_card'])
            
            if hasattr(self, 'scrollable_frame'):
                self.scrollable_frame.configure(bg=self.design.colors['bg_card'])
            
            # Update theme buttons if they exist
            if hasattr(self, 'light_btn') and hasattr(self, 'dark_btn'):
                self.update_theme_buttons()
            
            # Update header frames
            if hasattr(self, 'content'):
                self.update_header_frames()
                
        except Exception as e:
            print(f"Error updating content area theme: {e}")
    
    def update_header_frames(self):
        """Update header frame themes"""
        # Update content header frame
        for widget in self.content.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=self.design.colors['bg_card'])
                # Update header content frame
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        child.configure(bg=self.design.colors['bg_card'])
                        # Update labels in header
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Label):
                                grandchild.config(
                                    fg=self.design.colors['text_primary'],
                                    bg=self.design.colors['bg_card']
                                )
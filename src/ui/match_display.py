"""
Match Display Module
Contains logic for displaying matches, tournaments, and match cards.
"""

import tkinter as tk
from datetime import datetime
import threading
import time


class MatchDisplay:
    """Handles the display of matches, tournaments, and match cards."""
    
    def __init__(self, design_system):
        self.design = design_system
        self.batch_size = 10  # Number of matches to render per batch
        self.render_delay = 50  # Delay between batches in milliseconds
        self.is_rendering = False
        self.current_batch = 0
        self.all_tournaments = []
        self.scrollable_frame = None
        self.root = None  # Will be set when needed
        self.visible_matches = []  # Track visible match widgets
        self.match_height = 120  # Approximate height of each match card
        self.viewport_height = 0  # Height of visible area
    
    def display_tournaments(self, scrollable_frame, matches_by_tournament):
        """Display all tournaments with lazy loading for better performance"""
        self.scrollable_frame = scrollable_frame
        self.all_tournaments = list(matches_by_tournament.values())
        self.current_batch = 0
        self.is_rendering = True
        
        # Get root window reference
        self.root = scrollable_frame.winfo_toplevel()
        
        # Calculate total matches
        total_matches = sum(len(tournament['matches']) for tournament in self.all_tournaments)
        
        # Start lazy loading in a separate thread
        threading.Thread(target=self._lazy_render_tournaments, daemon=True).start()
        
        return total_matches
    
    def _lazy_render_tournaments(self):
        """Render tournaments in batches to prevent UI freezing"""
        try:
            for i, tournament_info in enumerate(self.all_tournaments):
                if not self.is_rendering:
                    break
                    
                # Add separator between tournaments
                if i > 0:
                    self.root.after(0, lambda: self.add_tournament_separator(self.scrollable_frame))
                    time.sleep(self.render_delay / 1000)
                
                # Render tournament with lazy loading
                self._render_tournament_lazy(tournament_info)
                
                # Small delay to keep UI responsive
                time.sleep(self.render_delay / 1000)
                
        except Exception as e:
            print(f"Error in lazy rendering: {e}")
        finally:
            self.is_rendering = False
    
    def _render_tournament_lazy(self, tournament_info):
        """Render a single tournament with lazy loading for matches"""
        # Tournament container
        tournament_container = tk.Frame(
            self.scrollable_frame,
            bg=self.design.colors['bg_card']
        )
        self.root.after(0, lambda: tournament_container.pack(fill=tk.X, padx=self.design.spacing['lg'], pady=self.design.spacing['md']))
        
        # Tournament header
        self.root.after(0, lambda: self._create_tournament_header(tournament_container, tournament_info))
        
        # Matches container
        matches_container = tk.Frame(tournament_container, bg=self.design.colors['bg_card'])
        self.root.after(0, lambda: matches_container.pack(fill=tk.X))
        
        # Group matches by status
        live_matches = []
        finished_matches = []
        upcoming_matches = []
        
        for match in tournament_info['matches']:
            status = match['status']['type']
            if status == 'inprogress':
                live_matches.append(match)
            elif status == 'finished':
                finished_matches.append(match)
            else:
                upcoming_matches.append(match)
        
        # Render match sections with lazy loading
        if live_matches:
            self.root.after(0, lambda: self._create_match_section_lazy("🔴 LIVE", live_matches, matches_container, 'live'))
        if finished_matches:
            self.root.after(0, lambda: self._create_match_section_lazy("✅ FINISHED", finished_matches, matches_container, 'finished'))
        if upcoming_matches:
            self.root.after(0, lambda: self._create_match_section_lazy("📅 UPCOMING", upcoming_matches, matches_container, 'upcoming'))
    
    def _create_tournament_header(self, parent, tournament_info):
        """Create tournament header"""
        # Tournament header with modern styling
        header_frame = tk.Frame(parent, bg=self.design.colors['bg_card'])
        header_frame.pack(fill=tk.X, pady=(0, self.design.spacing['md']))
        
        # Tournament name with accent
        title_frame = tk.Frame(header_frame, bg=self.design.colors['bg_card'])
        title_frame.pack(fill=tk.X)
        
        # Color accent bar
        accent_bar = tk.Frame(
            title_frame,
            bg=self.design.colors['primary'],
            width=4,
            height=24
        )
        accent_bar.pack(side=tk.LEFT, padx=(0, self.design.spacing['md']))
        
        tk.Label(
            title_frame,
            text=tournament_info['tournament'],
            font=self.design.fonts['headline'],
            fg=self.design.colors['text_primary'],
            bg=self.design.colors['bg_card'],
            anchor='w'
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Round info
        if tournament_info['round'] and tournament_info['round'] != 'Regular Season':
            tk.Label(
                header_frame,
                text=tournament_info['round'],
                font=self.design.fonts['caption'],
                fg=self.design.colors['text_secondary'],
                bg=self.design.colors['bg_card'],
                anchor='w'
            ).pack(fill=tk.X, pady=(self.design.spacing['xs'], 0))
    
    def _create_match_section_lazy(self, title, matches, parent, section_type):
        """Create a section for matches with lazy loading"""
        section_frame = tk.Frame(parent, bg=self.design.colors['bg_card'])
        section_frame.pack(fill=tk.X, pady=(0, self.design.spacing['md']))
        
        # Section header
        section_header = tk.Frame(section_frame, bg=self.design.colors['bg_card'])
        section_header.pack(fill=tk.X, pady=(0, self.design.spacing['sm']))
        
        tk.Label(
            section_header,
            text=title,
            font=self.design.fonts['label'],
            fg=self.design.get_section_color(section_type),
            bg=self.design.colors['bg_card'],
            anchor='w'
        ).pack(side=tk.LEFT)
        
        tk.Label(
            section_header,
            text=f"({len(matches)})",
            font=self.design.fonts['caption'],
            fg=self.design.colors['text_muted'],
            bg=self.design.colors['bg_card']
        ).pack(side=tk.LEFT, padx=(self.design.spacing['xs'], 0))
        
        # Matches grid
        matches_grid = tk.Frame(section_frame, bg=self.design.colors['bg_card'])
        matches_grid.pack(fill=tk.X)
        
        # Render matches in batches
        self._render_matches_batch(matches, matches_grid, section_type, 0)
    
    def _render_matches_batch(self, matches, parent, section_type, start_index):
        """Render a batch of matches with lazy loading"""
        end_index = min(start_index + self.batch_size, len(matches))
        
        for i in range(start_index, end_index):
            if not self.is_rendering:
                break
                
            # Create row frame for every 2 matches
            if (i - start_index) % 2 == 0:
                row_frame = tk.Frame(parent, bg=self.design.colors['bg_card'])
                row_frame.pack(fill=tk.X, pady=self.design.spacing['xs'])
            
            # Create match card
            self.create_modern_match_card(matches[i], row_frame, section_type)
        
        # If there are more matches, schedule the next batch
        if end_index < len(matches) and self.is_rendering:
            self.root.after(self.render_delay, 
                          lambda: self._render_matches_batch(matches, parent, section_type, end_index))
    
    def stop_rendering(self):
        """Stop the current rendering process"""
        self.is_rendering = False
    
    def setup_virtual_scrolling(self, canvas):
        """Setup virtual scrolling for better performance"""
        self.canvas = canvas
        self.viewport_height = canvas.winfo_height()
        
        # Bind scroll events
        canvas.bind('<Configure>', self.on_canvas_configure)
        canvas.bind('<Button-4>', self.on_mousewheel)  # Linux scroll up
        canvas.bind('<Button-5>', self.on_mousewheel)  # Linux scroll down
        canvas.bind('<MouseWheel>', self.on_mousewheel)  # Windows/Mac scroll
    
    def on_canvas_configure(self, event):
        """Handle canvas resize"""
        self.viewport_height = event.height
        self.update_visible_matches()
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        # Scroll the canvas
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        
        # Update visible matches after scrolling
        self.root.after(10, self.update_visible_matches)
    
    def update_visible_matches(self):
        """Update which matches are visible and should be rendered"""
        if not self.canvas:
            return
            
        # Get scroll position
        scroll_top = self.canvas.canvasy(0)
        scroll_bottom = scroll_top + self.viewport_height
        
        # Calculate which matches should be visible
        start_index = max(0, int(scroll_top // self.match_height) - 2)  # Add buffer
        end_index = min(len(self.all_tournaments), int(scroll_bottom // self.match_height) + 2)  # Add buffer
        
        # Hide matches outside viewport
        for i, match_widget in enumerate(self.visible_matches):
            if i < start_index or i >= end_index:
                if match_widget.winfo_exists():
                    match_widget.pack_forget()
            else:
                if match_widget.winfo_exists():
                    match_widget.pack(fill=tk.X, padx=self.design.spacing['lg'], pady=self.design.spacing['md'])
    
    def create_virtual_match_card(self, match, parent, section_type, index):
        """Create a virtual match card that can be shown/hidden"""
        # Create placeholder frame for virtual scrolling
        placeholder = tk.Frame(parent, height=self.match_height, bg=self.design.colors['bg_card'])
        
        # Store the actual match data
        placeholder.match_data = match
        placeholder.section_type = section_type
        placeholder.index = index
        
        # Only render if visible
        if self.is_match_visible(index):
            self.create_modern_match_card(match, placeholder, section_type)
        
        return placeholder
    
    def is_match_visible(self, index):
        """Check if a match at given index should be visible"""
        if not self.canvas:
            return True  # If no virtual scrolling, show all
            
        scroll_top = self.canvas.canvasy(0)
        scroll_bottom = scroll_top + self.viewport_height
        
        match_top = index * self.match_height
        match_bottom = match_top + self.match_height
        
        return not (match_bottom < scroll_top or match_top > scroll_bottom)
    
    def display_modern_tournament(self, parent, tournament_info):
        """Display tournament with modern card design"""
        # Tournament container
        tournament_container = tk.Frame(
            parent,
            bg=self.design.colors['bg_card']
        )
        tournament_container.pack(fill=tk.X, padx=self.design.spacing['lg'], pady=self.design.spacing['md'])
        
        # Tournament header with modern styling
        header_frame = tk.Frame(
            tournament_container,
            bg=self.design.colors['bg_card']
        )
        header_frame.pack(fill=tk.X, pady=(0, self.design.spacing['md']))
        
        # Tournament name with accent
        title_frame = tk.Frame(header_frame, bg=self.design.colors['bg_card'])
        title_frame.pack(fill=tk.X)
        
        # Color accent bar
        accent_bar = tk.Frame(
            title_frame,
            bg=self.design.colors['primary'],
            width=4,
            height=24
        )
        accent_bar.pack(side=tk.LEFT, padx=(0, self.design.spacing['md']))
        
        tk.Label(
            title_frame,
            text=tournament_info['tournament'],
            font=self.design.fonts['headline'],
            fg=self.design.colors['text_primary'],
            bg=self.design.colors['bg_card'],
            anchor='w'
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Round info
        if tournament_info['round'] and tournament_info['round'] != 'Regular Season':
            tk.Label(
                header_frame,
                text=tournament_info['round'],
                font=self.design.fonts['caption'],
                fg=self.design.colors['text_secondary'],
                bg=self.design.colors['bg_card'],
                anchor='w'
            ).pack(fill=tk.X, pady=(self.design.spacing['xs'], 0))
        
        # Matches container
        matches_container = tk.Frame(tournament_container, bg=self.design.colors['bg_card'])
        matches_container.pack(fill=tk.X)
        
        # Group matches by status
        live_matches = []
        finished_matches = []
        upcoming_matches = []
        
        for match in tournament_info['matches']:
            status = match['status']['type']
            if status == 'inprogress':
                live_matches.append(match)
            elif status == 'finished':
                finished_matches.append(match)
            else:
                upcoming_matches.append(match)
        
        # Display matches by priority (live first)
        if live_matches:
            self.create_match_section("🔴 LIVE", live_matches, matches_container, 'live')
        if finished_matches:
            self.create_match_section("✅ FINISHED", finished_matches, matches_container, 'finished')
        if upcoming_matches:
            self.create_match_section("📅 UPCOMING", upcoming_matches, matches_container, 'upcoming')
    
    def create_match_section(self, title, matches, parent, section_type):
        """Create a section for matches of the same status"""
        section_frame = tk.Frame(parent, bg=self.design.colors['bg_card'])
        section_frame.pack(fill=tk.X, pady=(0, self.design.spacing['md']))
        
        # Section header
        section_header = tk.Frame(section_frame, bg=self.design.colors['bg_card'])
        section_header.pack(fill=tk.X, pady=(0, self.design.spacing['sm']))
        
        tk.Label(
            section_header,
            text=title,
            font=self.design.fonts['label'],
            fg=self.design.get_section_color(section_type),
            bg=self.design.colors['bg_card'],
            anchor='w'
        ).pack(side=tk.LEFT)
        
        tk.Label(
            section_header,
            text=f"({len(matches)})",
            font=self.design.fonts['caption'],
            fg=self.design.colors['text_muted'],
            bg=self.design.colors['bg_card']
        ).pack(side=tk.LEFT, padx=(self.design.spacing['xs'], 0))
        
        # Matches grid
        matches_grid = tk.Frame(section_frame, bg=self.design.colors['bg_card'])
        matches_grid.pack(fill=tk.X)
        
        # Display matches in rows of 2
        for i in range(0, len(matches), 2):
            row_frame = tk.Frame(matches_grid, bg=self.design.colors['bg_card'])
            row_frame.pack(fill=tk.X, pady=self.design.spacing['xs'])
            
            # First match
            self.create_modern_match_card(matches[i], row_frame, section_type)
            
            # Second match if exists
            if i + 1 < len(matches):
                self.create_modern_match_card(matches[i + 1], row_frame, section_type)
    
    def create_modern_match_card(self, match, parent, section_type):
        """Create a modern match card with enhanced styling"""
        # Card container with hover effects
        card_container = tk.Frame(parent, bg=self.design.colors['bg_card'])
        card_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, self.design.spacing['sm']))
        
        # Main card with modern styling
        card = tk.Frame(
            card_container,
            bg=self.design.colors['bg_card'],
            relief=tk.FLAT,
            bd=1,
            highlightbackground=self.design.colors['border'],
            highlightthickness=1
        )
        card.pack(fill=tk.BOTH, expand=True, padx=self.design.spacing['xs'], pady=self.design.spacing['xs'])
        
        # Add hover effect
        self.setup_card_hover(card)
        
        # Status indicator bar
        status_color = self.design.get_section_color(section_type)
        status_bar = tk.Frame(card, bg=status_color, height=3)
        status_bar.pack(fill=tk.X)
        
        # Card content
        content = tk.Frame(card, bg=self.design.colors['bg_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=self.design.spacing['md'], pady=self.design.spacing['md'])
        
        # Match teams and score
        home_team = match["homeTeam"]["name"]
        away_team = match["awayTeam"]["name"]
        home_score = match["homeScore"].get("current", "-")
        away_score = match["awayScore"].get("current", "-")
        
        # Teams section
        teams_frame = tk.Frame(content, bg=self.design.colors['bg_card'])
        teams_frame.pack(fill=tk.X)
        
        # Home team
        home_frame = tk.Frame(teams_frame, bg=self.design.colors['bg_card'])
        home_frame.pack(fill=tk.X, pady=(0, self.design.spacing['xs']))
        
        # Team logo placeholder
        tk.Label(
            home_frame,
            text=home_team[:3].upper(),
            font=self.design.fonts['caption'],
            bg=self.design.colors['bg_primary'],
            fg=self.design.colors['primary'],
            width=4,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=(0, self.design.spacing['sm']))
        
        # Home team name
        home_label = tk.Label(
            home_frame,
            text=self.design.truncate_team_name(home_team),
            font=self.design.fonts['body_medium'],
            fg=self.design.colors['text_primary'],
            bg=self.design.colors['bg_card'],
            anchor='w'
        )
        home_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Home score
        home_score_label = None
        if section_type in ['live', 'finished']:
            home_score_label = tk.Label(
                home_frame,
                text=str(home_score),
                font=self.design.fonts['headline'],
                fg=self.design.colors['text_primary'],
                bg=self.design.colors['bg_card']
            )
            home_score_label.pack(side=tk.RIGHT)
        
        # Away team
        away_frame = tk.Frame(teams_frame, bg=self.design.colors['bg_card'])
        away_frame.pack(fill=tk.X, pady=(0, self.design.spacing['sm']))
        
        # Team logo placeholder
        tk.Label(
            away_frame,
            text=away_team[:3].upper(),
            font=self.design.fonts['caption'],
            bg=self.design.colors['bg_primary'],
            fg=self.design.colors['primary'],
            width=4,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=(0, self.design.spacing['sm']))
        
        # Away team name
        away_label = tk.Label(
            away_frame,
            text=self.design.truncate_team_name(away_team),
            font=self.design.fonts['body_medium'],
            fg=self.design.colors['text_primary'],
            bg=self.design.colors['bg_card'],
            anchor='w'
        )
        away_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Away score
        away_score_label = None
        if section_type in ['live', 'finished']:
            away_score_label = tk.Label(
                away_frame,
                text=str(away_score),
                font=self.design.fonts['headline'],
                fg=self.design.colors['text_primary'],
                bg=self.design.colors['bg_card']
            )
            away_score_label.pack(side=tk.RIGHT)
        
        # Status and time section
        status_frame = tk.Frame(content, bg=self.design.colors['bg_card'])
        status_frame.pack(fill=tk.X)
        
        # Status indicator
        self.create_match_status_indicator(match, status_frame, section_type)
        
        # Winner highlighting for finished matches
        if section_type == 'finished' and 'winnerCode' in match.get('status', {}) and home_score_label and away_score_label:
            self.highlight_winner(match, home_label, away_label, home_score_label, away_score_label)
    
    def create_match_status_indicator(self, match, parent, section_type):
        """Create modern status indicator"""
        status_container = tk.Frame(
            parent,
            bg=self.design.colors['bg_primary'],
            relief=tk.FLAT
        )
        status_container.pack(fill=tk.X, ipady=self.design.spacing['xs'])
        
        if section_type == 'live':
            # Live indicator with animation
            live_dot = tk.Label(
                status_container,
                text="●",
                font=self.design.fonts['body_medium'],
                fg=self.design.colors['live'],
                bg=self.design.colors['bg_primary']
            )
            live_dot.pack(side=tk.LEFT, padx=(self.design.spacing['sm'], self.design.spacing['xs']))
            
            minute = match.get('time', {}).get('minute', '')
            status_text = f"LIVE {minute}'" if minute else "LIVE"
            
            tk.Label(
                status_container,
                text=status_text,
                font=self.design.fonts['caption'],
                fg=self.design.colors['live'],
                bg=self.design.colors['bg_primary']
            ).pack(side=tk.LEFT)
            
        elif section_type == 'finished':
            tk.Label(
                status_container,
                text="FULL TIME",
                font=self.design.fonts['caption'],
                fg=self.design.colors['finished'],
                bg=self.design.colors['bg_primary']
            ).pack(side=tk.LEFT, padx=self.design.spacing['sm'])
            
        else:  # upcoming
            try:
                match_time = datetime.fromtimestamp(match['startTimestamp'])
                time_str = match_time.strftime('%H:%M')
                date_str = match_time.strftime('%m/%d') if match_time.date() != datetime.now().date() else "Today"
                
                tk.Label(
                    status_container,
                    text=f"{date_str} {time_str}",
                    font=self.design.fonts['caption'],
                    fg=self.design.colors['upcoming'],
                    bg=self.design.colors['bg_primary']
                ).pack(side=tk.LEFT, padx=self.design.spacing['sm'])
            except:
                tk.Label(
                    status_container,
                    text=match.get('status', {}).get('description', 'Scheduled'),
                    font=self.design.fonts['caption'],
                    fg=self.design.colors['upcoming'],
                    bg=self.design.colors['bg_primary']
                ).pack(side=tk.LEFT, padx=self.design.spacing['sm'])
    
    def add_tournament_separator(self, parent):
        """Add visual separator between tournaments"""
        separator_frame = tk.Frame(
            parent,
            bg=self.design.colors['bg_card'],
            height=self.design.spacing['xl']
        )
        separator_frame.pack(fill=tk.X, padx=self.design.spacing['lg'])
        
        # Gradient-like separator
        tk.Frame(
            separator_frame,
            bg=self.design.colors['border'],
            height=1
        ).pack(expand=True, fill=tk.X, pady=self.design.spacing['lg'])
    
    def setup_card_hover(self, card):
        """Setup hover effects for match cards"""
        def on_enter(e):
            card.config(highlightbackground=self.design.colors['primary'], highlightthickness=2)
        
        def on_leave(e):
            card.config(highlightbackground=self.design.colors['border'], highlightthickness=1)
        
        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)
    
    def highlight_winner(self, match, home_label, away_label, home_score_label, away_score_label):
        """Highlight winner in finished matches"""
        winner_code = match.get('status', {}).get('winnerCode', 0)
        
        if winner_code == 1:  # Home win
            home_label.config(fg=self.design.colors['finished'], font=self.design.fonts['body_medium'] + ('bold',))
            home_score_label.config(fg=self.design.colors['finished'], font=self.design.fonts['headline'] + ('bold',))
        elif winner_code == 2:  # Away win
            away_label.config(fg=self.design.colors['finished'], font=self.design.fonts['body_medium'] + ('bold',))
            away_score_label.config(fg=self.design.colors['finished'], font=self.design.fonts['headline'] + ('bold',))
    
    def update_theme(self, design_system=None):
        """Update component colors when theme changes"""
        if design_system:
            self.design = design_system
        # The actual display elements are recreated when needed, so we don't need to update them here
        # The design system reference has been updated, so new elements will use the correct colors
"""
Match Display Module
Contains logic for displaying matches, tournaments, and match cards.
"""

import tkinter as tk
from datetime import datetime


class MatchDisplay:
    """Handles the display of matches, tournaments, and match cards."""
    
    def __init__(self, design_system):
        self.design = design_system
    
    def display_tournaments(self, scrollable_frame, matches_by_tournament):
        """Display all tournaments with modern styling"""
        total_matches = 0
        tournament_list = list(matches_by_tournament.values())
        
        for i, tournament_info in enumerate(tournament_list):
            if i > 0:
                self.add_tournament_separator(scrollable_frame)
            
            self.display_modern_tournament(scrollable_frame, tournament_info)
            total_matches += len(tournament_info['matches'])
        
        return total_matches
    
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
import tkinter as tk
from tkinter import ttk, messagebox
from scraper.match_scraper import MatchScraper
from datetime import datetime
import json
import threading
import math
import os

class FootballApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Football Scores Pro")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Configure styles and colors
        self.setup_design_system()
        
        # Main container with gradient background
        self.main_container = tk.Frame(root, bg=self.colors['bg_primary'])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_modern_header()
        
        # Content area with card design
        self.content_frame = tk.Frame(
            self.main_container, 
            bg=self.colors['bg_secondary'],
            relief=tk.FLAT
        )
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.content_frame.pack_propagate(False)
        
        # Left sidebar with modern design
        self.create_modern_sidebar()
        
        # Right content area
        self.create_modern_content()
        
        # Modern status bar
        self.create_modern_status_bar()
        
        # Threading control
        self.is_running = False
        self.animation_active = True
        
        # Start background animations
        self.start_live_animations()
        
        # Automatically fetch matches when the app starts
        self.root.after(1000, self.fetch_matches)
    
    def setup_design_system(self):
        """Setup modern design system with colors, fonts, and spacing"""
        # Modern Color Palette
        self.colors = {
            # Primary Colors
            'primary': '#0066FF',           # Electric Blue
            'success': '#00C851',           # Stadium Green
            'live': '#FF1744',              # Live Red
            'warning': '#FFD700',           # Championship Gold
            'danger': '#FF6B35',            # Sunset Orange
            
            # Background Colors
            'bg_primary': '#F8F9FA',        # Cloud White background
            'bg_secondary': '#FFFFFF',       # Pure white
            'bg_card': '#FFFFFF',           # Card backgrounds
            'bg_sidebar': '#FFFFFF',        # Sidebar background
            'bg_header': '#1B1B2F',         # Midnight Navy
            
            # Text Colors
            'text_primary': '#1B1B2F',      # Midnight Navy
            'text_secondary': '#6C757D',    # Steel Gray
            'text_muted': '#ADB5BD',        # Light gray
            'text_white': '#FFFFFF',        # White text
            
            # State Colors
            'finished': '#4CAF50',          # Victory Green
            'upcoming': '#3F51B5',          # Upcoming Indigo
            'draw': '#FFC107',              # Draw Amber
            
            # UI Colors
            'border': '#DEE2E6',            # Light border
            'shadow': 'rgba(0,0,0,0.1)',    # Subtle shadow
            'hover': '#F8F9FA',             # Hover state
            'active': '#E3F2FD',            # Active state
        }
        
        # Typography Scale
        self.fonts = {
            'display_large': ('Inter', 32, 'bold'),
            'display_medium': ('Inter', 24, 'bold'),
            'headline': ('Inter', 18, 'normal'),
            'body_large': ('Inter', 16, 'normal'),
            'body_medium': ('Inter', 14, 'normal'),
            'caption': ('Inter', 12, 'normal'),
            'label': ('Inter', 11, 'bold'),
        }
        
        # Spacing System (8px grid)
        self.spacing = {
            'xs': 4,
            'sm': 8,
            'md': 16,
            'lg': 24,
            'xl': 32,
            'xxl': 48
        }
        
        # Configure ttk styles
        self.setup_ttk_styles()
    
    def setup_ttk_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Modern button styles
        style.configure('Modern.TButton',
                       font=self.fonts['body_medium'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 10))
        
        style.map('Modern.TButton',
                 background=[('active', self.colors['primary']),
                            ('pressed', self.colors['primary'])])
        
        # Primary button style
        style.configure('Primary.TButton',
                       font=self.fonts['body_medium'],
                       background=self.colors['primary'],
                       foreground=self.colors['text_white'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(24, 12))
        
        # Secondary button style  
        style.configure('Secondary.TButton',
                       font=self.fonts['body_medium'],
                       background=self.colors['bg_card'],
                       foreground=self.colors['primary'],
                       borderwidth=1,
                       focuscolor='none',
                       relief='solid',
                       padding=(20, 10))
        
        # Search entry style
        style.configure('Search.TEntry',
                       font=self.fonts['body_medium'],
                       borderwidth=0,
                       relief='flat',
                       padding=(16, 12))
    
    def create_modern_header(self):
        """Create modern header with gradient background"""
        header = tk.Frame(
            self.main_container,
            bg=self.colors['bg_header'],
            height=80
        )
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Left section with logo and title
        left_section = tk.Frame(header, bg=self.colors['bg_header'])
        left_section.pack(side=tk.LEFT, fill=tk.Y, padx=self.spacing['xl'])
        
        # Logo and title container
        logo_container = tk.Frame(left_section, bg=self.colors['bg_header'])
        logo_container.pack(expand=True)
        
        # Modern logo
        logo_label = tk.Label(
            logo_container,
            text="⚽",
            font=('Inter', 28),
            bg=self.colors['bg_header'],
            fg=self.colors['success']
        )
        logo_label.pack(side=tk.LEFT, padx=(0, self.spacing['md']))
        
        # App title with modern typography
        title_label = tk.Label(
            logo_container,
            text="FOOTBALL SCORES PRO",
            font=self.fonts['display_medium'],
            bg=self.colors['bg_header'],
            fg=self.colors['text_white']
        )
        title_label.pack(side=tk.LEFT)
        
        # Right section with date and live indicator
        right_section = tk.Frame(header, bg=self.colors['bg_header'])
        right_section.pack(side=tk.RIGHT, fill=tk.Y, padx=self.spacing['xl'])
        
        # Live indicator
        self.live_indicator = tk.Frame(right_section, bg=self.colors['bg_header'])
        self.live_indicator.pack(side=tk.RIGHT, padx=(self.spacing['lg'], 0))
        
        self.live_dot = tk.Label(
            self.live_indicator,
            text="●",
            font=self.fonts['body_large'],
            bg=self.colors['bg_header'],
            fg=self.colors['live']
        )
        self.live_dot.pack(side=tk.LEFT, padx=(0, self.spacing['sm']))
        
        tk.Label(
            self.live_indicator,
            text="LIVE",
            font=self.fonts['label'],
            bg=self.colors['bg_header'],
            fg=self.colors['text_white']
        ).pack(side=tk.LEFT)
        
        # Date display
        self.date_var = tk.StringVar()
        self.date_var.set(datetime.now().strftime("%A, %B %d, %Y"))
        
        date_label = tk.Label(
            right_section,
            textvariable=self.date_var,
            font=self.fonts['body_medium'],
            bg=self.colors['bg_header'],
            fg=self.colors['text_muted']
        )
        date_label.pack(side=tk.RIGHT, padx=(0, self.spacing['lg']))
    
    def create_modern_sidebar(self):
        """Create modern sidebar with card design"""
        # Sidebar container
        sidebar_container = tk.Frame(
            self.content_frame,
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
            bg=self.colors['bg_sidebar']
        )
        search_section.pack(fill=tk.X, padx=self.spacing['lg'], pady=self.spacing['lg'])
        
        # Search container with pill shape
        search_container = tk.Frame(
            search_section,
            bg=self.colors['bg_primary'],
            relief=tk.FLAT,
            bd=0
        )
        search_container.pack(fill=tk.X, ipady=self.spacing['sm'])
        
        # Search icon
        search_icon = tk.Label(
            search_container,
            text="🔍",
            font=self.fonts['body_medium'],
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary']
        )
        search_icon.pack(side=tk.LEFT, padx=(self.spacing['md'], self.spacing['sm']))
        
        # Search entry
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_container,
            textvariable=self.search_var,
            font=self.fonts['body_medium'],
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary'],
            border=0,
            relief=tk.FLAT
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, self.spacing['md']))
        
        # Placeholder behavior
        search_entry.insert(0, "Search matches...")
        search_entry.bind('<FocusIn>', lambda e: self.on_search_focus_in(e))
        search_entry.bind('<FocusOut>', lambda e: self.on_search_focus_out(e))
    
    def create_modern_navigation(self, parent):
        """Create modern navigation menu"""
        nav_section = tk.Frame(parent, bg=self.colors['bg_sidebar'])
        nav_section.pack(fill=tk.X, pady=self.spacing['md'])
        
        # Navigation items with modern styling
        nav_items = [
            ("📊", "Live Matches", self.show_live_matches, True),
            ("📅", "Fixtures", self.show_fixtures, False),
            ("⭐", "Favorites", self.show_favorites, False),
            ("⚙️", "Settings", self.show_settings, False)
        ]
        
        self.nav_buttons = []
        for icon, text, command, active in nav_items:
            btn_frame = tk.Frame(nav_section, bg=self.colors['bg_sidebar'])
            btn_frame.pack(fill=tk.X, padx=self.spacing['md'], pady=self.spacing['xs'])
            
            if active:
                btn_frame.config(bg=self.colors['active'])
                
            btn = tk.Button(
                btn_frame,
                text=f"{icon}  {text}",
                font=self.fonts['body_medium'],
                bg=self.colors['active'] if active else self.colors['bg_sidebar'],
                fg=self.colors['primary'] if active else self.colors['text_primary'],
                bd=0,
                relief=tk.FLAT,
                anchor='w',
                padx=self.spacing['lg'],
                pady=self.spacing['md'],
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
            bg=self.colors['border'], 
            height=1
        )
        separator.pack(fill=tk.X, padx=self.spacing['lg'], pady=self.spacing['lg'])
    
    def create_modern_actions(self, parent):
        """Create modern action buttons"""
        action_section = tk.Frame(parent, bg=self.colors['bg_sidebar'])
        action_section.pack(fill=tk.X, padx=self.spacing['lg'], pady=self.spacing['md'])
        
        # Fetch button with modern styling
        self.fetch_btn = tk.Button(
            action_section,
            text="🔄  Fetch Matches",
            font=self.fonts['body_medium'],
            bg=self.colors['success'],
            fg=self.colors['text_white'],
            bd=0,
            relief=tk.FLAT,
            padx=self.spacing['lg'],
            pady=self.spacing['md'],
            command=self.fetch_matches,
            cursor='hand2'
        )
        self.fetch_btn.pack(fill=tk.X, pady=(0, self.spacing['sm']))
        
        # Stop button
        self.stop_btn = tk.Button(
            action_section,
            text="⏹  Stop",
            font=self.fonts['body_medium'],
            bg=self.colors['bg_card'],
            fg=self.colors['danger'],
            bd=1,
            relief=tk.SOLID,
            padx=self.spacing['lg'],
            pady=self.spacing['md'],
            command=self.stop_fetching,
            state=tk.DISABLED,
            cursor='hand2'
        )
        self.stop_btn.pack(fill=tk.X)
        
        # Button hover effects
        self.setup_button_hover_effects()
    
    def create_sidebar_status(self, parent):
        """Create sidebar status section"""
        status_section = tk.Frame(parent, bg=self.colors['bg_sidebar'])
        status_section.pack(side=tk.BOTTOM, fill=tk.X, padx=self.spacing['lg'], pady=self.spacing['lg'])
        
        # Status indicator
        status_container = tk.Frame(
            status_section,
            bg=self.colors['bg_primary'],
            relief=tk.FLAT
        )
        status_container.pack(fill=tk.X, pady=self.spacing['sm'])
        
        # Status dot
        self.status_dot = tk.Label(
            status_container,
            text="●",
            font=self.fonts['body_medium'],
            bg=self.colors['bg_primary'],
            fg=self.colors['success']
        )
        self.status_dot.pack(side=tk.LEFT, padx=(self.spacing['md'], self.spacing['sm']))
        
        # Status text
        self.status_label = tk.Label(
            status_container,
            text="Ready to fetch matches",
            font=self.fonts['caption'],
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_primary'],
            anchor='w'
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, self.spacing['md']))
    
    def create_modern_content(self):
        """Create modern content area"""
        content = tk.Frame(
            self.content_frame, 
            bg=self.colors['bg_card'],
            relief=tk.FLAT,
            bd=1,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Content header
        header = tk.Frame(content, bg=self.colors['bg_card'], height=80)
        header.pack(fill=tk.X, padx=self.spacing['xl'], pady=self.spacing['lg'])
        header.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header, bg=self.colors['bg_card'])
        header_content.pack(expand=True)
        
        self.content_title = tk.Label(
            header_content,
            text="Live Matches",
            font=self.fonts['display_medium'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card'],
            anchor='w'
        )
        self.content_title.pack(fill=tk.X)
        
        # Subtitle
        self.content_subtitle = tk.Label(
            header_content,
            text="Real-time football scores and updates",
            font=self.fonts['body_medium'],
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_card'],
            anchor='w'
        )
        self.content_subtitle.pack(fill=tk.X, pady=(self.spacing['xs'], 0))
        
        # Matches container with modern scrolling
        self.matches_container = tk.Frame(content, bg=self.colors['bg_card'])
        self.matches_container.pack(fill=tk.BOTH, expand=True, padx=self.spacing['xl'], pady=(0, self.spacing['lg']))
        
        # Custom scrollable area
        self.setup_modern_scrollable_area()
        
        # Show modern empty state
        self.show_modern_empty_state()
    
    def setup_modern_scrollable_area(self):
        """Setup modern scrollable area with custom styling"""
        # Canvas for scrolling
        self.canvas = tk.Canvas(
            self.matches_container,
            bg=self.colors['bg_card'],
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
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['bg_card'])
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
    
    def create_modern_status_bar(self):
        """Create modern status bar"""
        status_container = tk.Frame(
            self.main_container,
            bg=self.colors['primary'],
            height=40
        )
        status_container.pack(side=tk.BOTTOM, fill=tk.X)
        status_container.pack_propagate(False)
        
        # Status content
        status_content = tk.Frame(status_container, bg=self.colors['primary'])
        status_content.pack(expand=True, padx=self.spacing['xl'])
        
        # Status text
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(
            status_content,
            textvariable=self.status_var,
            font=self.fonts['body_medium'],
            fg=self.colors['text_white'],
            bg=self.colors['primary'],
            anchor='w'
        )
        self.status_bar.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.status_var.set("Ready")
        
        # Match count
        self.match_count_label = tk.Label(
            status_content,
            text="0 matches",
            font=self.fonts['caption'],
            fg=self.colors['text_white'],
            bg=self.colors['primary'],
            anchor='e'
        )
        self.match_count_label.pack(side=tk.RIGHT)
    
    def show_modern_empty_state(self, message="No matches available", subtitle="Click 'Fetch Matches' to get the latest scores"):
        """Show modern empty state"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        empty_container = tk.Frame(self.scrollable_frame, bg=self.colors['bg_card'])
        empty_container.pack(expand=True, fill=tk.BOTH)
        
        # Center the empty state
        empty_frame = tk.Frame(empty_container, bg=self.colors['bg_card'])
        empty_frame.pack(expand=True)
        
        # Large icon
        tk.Label(
            empty_frame,
            text="⚽",
            font=('Inter', 64),
            fg=self.colors['text_muted'],
            bg=self.colors['bg_card']
        ).pack(pady=(0, self.spacing['lg']))
        
        # Main message
        tk.Label(
            empty_frame,
            text=message,
            font=self.fonts['headline'],
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_card']
        ).pack(pady=(0, self.spacing['sm']))
        
        # Subtitle
        tk.Label(
            empty_frame,
            text=subtitle,
            font=self.fonts['body_medium'],
            fg=self.colors['text_muted'],
            bg=self.colors['bg_card']
        ).pack()
    
    def fetch_matches(self):
        """Start fetching matches with modern UI updates"""
        if self.is_running:
            return
            
        self.is_running = True
        self.fetch_btn.config(state=tk.DISABLED, bg=self.colors['text_muted'])
        self.stop_btn.config(state=tk.NORMAL, bg=self.colors['danger'], fg=self.colors['text_white'])
        
        # Update status with modern styling
        self.update_status("Fetching matches...", self.colors['primary'], "●")
        self.status_var.set("Fetching live matches...")
        
        # Show loading state
        self.show_modern_loading_state()
        
        try:
            # Run the scraper in a separate thread
            self.scraper = MatchScraper()
            self.scraper_thread = threading.Thread(target=self.run_scraper)
            self.scraper_thread.daemon = True
            self.scraper_thread.start()
            
            # Check scraper status periodically
            self.check_scraper_status()
        except Exception as e:
            self.show_error(f"Failed to start scraper: {str(e)}")
            self.cleanup()
    
    def show_modern_loading_state(self):
        """Show modern loading state with skeleton screens"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        loading_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg_card'])
        loading_frame.pack(fill=tk.BOTH, expand=True, padx=self.spacing['lg'], pady=self.spacing['lg'])
        
        # Create skeleton cards
        for i in range(3):
            self.create_skeleton_card(loading_frame)
    
    def create_skeleton_card(self, parent):
        """Create skeleton loading card"""
        skeleton_card = tk.Frame(
            parent,
            bg=self.colors['bg_primary'],
            relief=tk.FLAT,
            bd=1,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        skeleton_card.pack(fill=tk.X, pady=self.spacing['sm'])
        
        # Skeleton content
        content = tk.Frame(skeleton_card, bg=self.colors['bg_primary'])
        content.pack(fill=tk.X, padx=self.spacing['lg'], pady=self.spacing['lg'])
        
        # Tournament name skeleton
        tk.Frame(
            content,
            bg=self.colors['border'],
            height=20,
            width=200
        ).pack(anchor='w', pady=(0, self.spacing['md']))
        
        # Match skeleton
        match_frame = tk.Frame(content, bg=self.colors['bg_primary'])
        match_frame.pack(fill=tk.X)
        
        for _ in range(2):
            tk.Frame(
                match_frame,
                bg=self.colors['border'],
                height=15,
                width=150
            ).pack(anchor='w', pady=self.spacing['xs'])
    
    def run_scraper(self):
        """Run the scraper and process results"""
        try:
            # Initialize the scraper with the output path
            self.scraper = MatchScraper(output_path=os.path.join("data", "events.json"))
            
            # Run the scraper
            success = self.scraper.run()
            
            # Schedule UI updates on the main thread
            if success and hasattr(self.scraper, 'json_data') and self.scraper.json_data:
                self.root.after(0, self.process_modern_results)
            else:
                error_msg = "Failed to fetch matches. Please check your internet connection and try again."
                if hasattr(self.scraper, 'last_error'):
                    error_msg = f"Error: {self.scraper.last_error}"
                self.root.after(0, lambda: self.show_error(error_msg))
        except Exception as e:
            error_msg = f"An unexpected error occurred: {str(e)}"
            self.root.after(0, lambda: self.show_error(error_msg))
    
    def process_modern_results(self):
        """Process and display results with modern UI"""
        try:
            # Clear previous results
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            
            # Get data directly from the scraper if available
            if hasattr(self.scraper, 'json_data') and self.scraper.json_data:
                data = self.scraper.json_data
            else:
                # Fallback to loading from file
                try:
                    with open(os.path.join('data', 'events.json'), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except FileNotFoundError:
                    self.show_modern_empty_state("No match data available")
                    return
                
            if 'events' in data and data['events']:
                # Group matches by tournament
                matches_by_tournament = {}
                
                for event in data['events']:
                    tournament_name = event['tournament']['name']
                    round_info = event.get('roundInfo', {})
                    round_name = round_info.get('round', 'Regular Season')
                    
                    key = f"{tournament_name}"
                    
                    if key not in matches_by_tournament:
                        matches_by_tournament[key] = {
                            'tournament': tournament_name,
                            'round': round_name,
                            'matches': []
                        }
                    
                    matches_by_tournament[key]['matches'].append(event)
                
                # Display all tournaments with modern styling
                total_matches = 0
                tournament_list = list(matches_by_tournament.values())
                for i, tournament_info in enumerate(tournament_list):
                    if i > 0:
                        self.add_tournament_separator()
                    
                    self.display_modern_tournament(tournament_info)
                    total_matches += len(tournament_info['matches'])
                
                print(f"Displayed {len(tournament_list)} tournaments with {total_matches} matches")
                
                # Update status
                self.update_status(f"Showing {total_matches} matches", self.colors['success'], "●")
                self.status_var.set(f"Successfully loaded {total_matches} matches")
                self.match_count_label.config(text=f"{total_matches} matches")
                
            else:
                self.show_modern_empty_state("No matches available")
                self.update_status("No matches found", self.colors['warning'], "●")
                
        except Exception as e:
            self.show_error(f"Error processing results: {str(e)}")
        finally:
            self.cleanup()
    
    def display_modern_tournament(self, tournament_info):
        """Display tournament with modern card design"""
        # Tournament container
        tournament_container = tk.Frame(
            self.scrollable_frame,
            bg=self.colors['bg_card']
        )
        tournament_container.pack(fill=tk.X, padx=self.spacing['lg'], pady=self.spacing['md'])
        
        # Tournament header with modern styling
        header_frame = tk.Frame(
            tournament_container,
            bg=self.colors['bg_card']
        )
        header_frame.pack(fill=tk.X, pady=(0, self.spacing['md']))
        
        # Tournament name with accent
        title_frame = tk.Frame(header_frame, bg=self.colors['bg_card'])
        title_frame.pack(fill=tk.X)
        
        # Color accent bar
        accent_bar = tk.Frame(
            title_frame,
            bg=self.colors['primary'],
            width=4,
            height=24
        )
        accent_bar.pack(side=tk.LEFT, padx=(0, self.spacing['md']))
        
        tk.Label(
            title_frame,
            text=tournament_info['tournament'],
            font=self.fonts['headline'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card'],
            anchor='w'
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Round info
        if tournament_info['round'] and tournament_info['round'] != 'Regular Season':
            tk.Label(
                header_frame,
                text=tournament_info['round'],
                font=self.fonts['caption'],
                fg=self.colors['text_secondary'],
                bg=self.colors['bg_card'],
                anchor='w'
            ).pack(fill=tk.X, pady=(self.spacing['xs'], 0))
        
        # Matches container
        matches_container = tk.Frame(tournament_container, bg=self.colors['bg_card'])
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
        section_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        section_frame.pack(fill=tk.X, pady=(0, self.spacing['md']))
        
        # Section header
        section_header = tk.Frame(section_frame, bg=self.colors['bg_card'])
        section_header.pack(fill=tk.X, pady=(0, self.spacing['sm']))
        
        tk.Label(
            section_header,
            text=title,
            font=self.fonts['label'],
            fg=self.get_section_color(section_type),
            bg=self.colors['bg_card'],
            anchor='w'
        ).pack(side=tk.LEFT)
        
        tk.Label(
            section_header,
            text=f"({len(matches)})",
            font=self.fonts['caption'],
            fg=self.colors['text_muted'],
            bg=self.colors['bg_card']
        ).pack(side=tk.LEFT, padx=(self.spacing['xs'], 0))
        
        # Matches grid
        matches_grid = tk.Frame(section_frame, bg=self.colors['bg_card'])
        matches_grid.pack(fill=tk.X)
        
        # Display matches in rows of 2
        for i in range(0, len(matches), 2):
            row_frame = tk.Frame(matches_grid, bg=self.colors['bg_card'])
            row_frame.pack(fill=tk.X, pady=self.spacing['xs'])
            
            # First match
            self.create_modern_match_card(matches[i], row_frame, section_type)
            
            # Second match if exists
            if i + 1 < len(matches):
                self.create_modern_match_card(matches[i + 1], row_frame, section_type)
    
    def create_modern_match_card(self, match, parent, section_type):
        """Create a modern match card with enhanced styling"""
        # Card container with hover effects
        card_container = tk.Frame(parent, bg=self.colors['bg_card'])
        card_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, self.spacing['sm']))
        
        # Main card with modern styling
        card = tk.Frame(
            card_container,
            bg=self.colors['bg_card'],
            relief=tk.FLAT,
            bd=1,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        card.pack(fill=tk.BOTH, expand=True, padx=self.spacing['xs'], pady=self.spacing['xs'])
        
        # Add hover effect
        self.setup_card_hover(card)
        
        # Status indicator bar
        status_color = self.get_section_color(section_type)
        status_bar = tk.Frame(card, bg=status_color, height=3)
        status_bar.pack(fill=tk.X)
        
        # Card content
        content = tk.Frame(card, bg=self.colors['bg_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=self.spacing['md'], pady=self.spacing['md'])
        
        # Match teams and score
        home_team = match["homeTeam"]["name"]
        away_team = match["awayTeam"]["name"]
        home_score = match["homeScore"].get("current", "-")
        away_score = match["awayScore"].get("current", "-")
        
        # Teams section
        teams_frame = tk.Frame(content, bg=self.colors['bg_card'])
        teams_frame.pack(fill=tk.X)
        
        # Home team
        home_frame = tk.Frame(teams_frame, bg=self.colors['bg_card'])
        home_frame.pack(fill=tk.X, pady=(0, self.spacing['xs']))
        
        # Team logo placeholder
        tk.Label(
            home_frame,
            text=home_team[:3].upper(),
            font=self.fonts['caption'],
            bg=self.colors['bg_primary'],
            fg=self.colors['primary'],
            width=4,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=(0, self.spacing['sm']))
        
        # Home team name
        home_label = tk.Label(
            home_frame,
            text=self.truncate_team_name(home_team),
            font=self.fonts['body_medium'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card'],
            anchor='w'
        )
        home_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Home score
        if section_type in ['live', 'finished']:
            home_score_label = tk.Label(
                home_frame,
                text=str(home_score),
                font=self.fonts['headline'],
                fg=self.colors['text_primary'],
                bg=self.colors['bg_card']
            )
            home_score_label.pack(side=tk.RIGHT)
        
        # Away team
        away_frame = tk.Frame(teams_frame, bg=self.colors['bg_card'])
        away_frame.pack(fill=tk.X, pady=(0, self.spacing['sm']))
        
        # Team logo placeholder
        tk.Label(
            away_frame,
            text=away_team[:3].upper(),
            font=self.fonts['caption'],
            bg=self.colors['bg_primary'],
            fg=self.colors['primary'],
            width=4,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=(0, self.spacing['sm']))
        
        # Away team name
        away_label = tk.Label(
            away_frame,
            text=self.truncate_team_name(away_team),
            font=self.fonts['body_medium'],
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card'],
            anchor='w'
        )
        away_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Away score
        if section_type in ['live', 'finished']:
            away_score_label = tk.Label(
                away_frame,
                text=str(away_score),
                font=self.fonts['headline'],
                fg=self.colors['text_primary'],
                bg=self.colors['bg_card']
            )
            away_score_label.pack(side=tk.RIGHT)
        
        # Status and time section
        status_frame = tk.Frame(content, bg=self.colors['bg_card'])
        status_frame.pack(fill=tk.X)
        
        # Status indicator
        self.create_match_status_indicator(match, status_frame, section_type)
        
        # Winner highlighting for finished matches
        if section_type == 'finished' and 'winnerCode' in match.get('status', {}):
            self.highlight_winner(match, home_label, away_label, home_score_label, away_score_label)
    
    def create_match_status_indicator(self, match, parent, section_type):
        """Create modern status indicator"""
        status_container = tk.Frame(
            parent,
            bg=self.colors['bg_primary'],
            relief=tk.FLAT
        )
        status_container.pack(fill=tk.X, ipady=self.spacing['xs'])
        
        if section_type == 'live':
            # Live indicator with animation
            live_dot = tk.Label(
                status_container,
                text="●",
                font=self.fonts['body_medium'],
                fg=self.colors['live'],
                bg=self.colors['bg_primary']
            )
            live_dot.pack(side=tk.LEFT, padx=(self.spacing['sm'], self.spacing['xs']))
            
            minute = match.get('time', {}).get('minute', '')
            status_text = f"LIVE {minute}'" if minute else "LIVE"
            
            tk.Label(
                status_container,
                text=status_text,
                font=self.fonts['caption'],
                fg=self.colors['live'],
                bg=self.colors['bg_primary']
            ).pack(side=tk.LEFT)
            
        elif section_type == 'finished':
            tk.Label(
                status_container,
                text="FULL TIME",
                font=self.fonts['caption'],
                fg=self.colors['finished'],
                bg=self.colors['bg_primary']
            ).pack(side=tk.LEFT, padx=self.spacing['sm'])
            
        else:  # upcoming
            try:
                match_time = datetime.fromtimestamp(match['startTimestamp'])
                time_str = match_time.strftime('%H:%M')
                date_str = match_time.strftime('%m/%d') if match_time.date() != datetime.now().date() else "Today"
                
                tk.Label(
                    status_container,
                    text=f"{date_str} {time_str}",
                    font=self.fonts['caption'],
                    fg=self.colors['upcoming'],
                    bg=self.colors['bg_primary']
                ).pack(side=tk.LEFT, padx=self.spacing['sm'])
            except:
                tk.Label(
                    status_container,
                    text=match.get('status', {}).get('description', 'Scheduled'),
                    font=self.fonts['caption'],
                    fg=self.colors['upcoming'],
                    bg=self.colors['bg_primary']
                ).pack(side=tk.LEFT, padx=self.spacing['sm'])
    
    def add_tournament_separator(self):
        """Add visual separator between tournaments"""
        separator_frame = tk.Frame(
            self.scrollable_frame,
            bg=self.colors['bg_card'],
            height=self.spacing['xl']
        )
        separator_frame.pack(fill=tk.X, padx=self.spacing['lg'])
        
        # Gradient-like separator
        tk.Frame(
            separator_frame,
            bg=self.colors['border'],
            height=1
        ).pack(expand=True, fill=tk.X, pady=self.spacing['lg'])
    
    # Helper methods
    def get_section_color(self, section_type):
        """Get color for section type"""
        colors = {
            'live': self.colors['live'],
            'finished': self.colors['finished'],
            'upcoming': self.colors['upcoming']
        }
        return colors.get(section_type, self.colors['primary'])
    
    def truncate_team_name(self, name, max_length=20):
        """Truncate team name for display"""
        return name[:max_length] + '...' if len(name) > max_length else name
    
    def highlight_winner(self, match, home_label, away_label, home_score_label, away_score_label):
        """Highlight winner in finished matches"""
        winner_code = match.get('status', {}).get('winnerCode', 0)
        
        if winner_code == 1:  # Home win
            home_label.config(fg=self.colors['finished'], font=self.fonts['body_medium'] + ('bold',))
            home_score_label.config(fg=self.colors['finished'], font=self.fonts['headline'] + ('bold',))
        elif winner_code == 2:  # Away win
            away_label.config(fg=self.colors['finished'], font=self.fonts['body_medium'] + ('bold',))
            away_score_label.config(fg=self.colors['finished'], font=self.fonts['headline'] + ('bold',))
    
    def setup_card_hover(self, card):
        """Setup hover effects for match cards"""
        original_bg = card.cget('bg')
        
        def on_enter(e):
            card.config(highlightbackground=self.colors['primary'], highlightthickness=2)
        
        def on_leave(e):
            card.config(highlightbackground=self.colors['border'], highlightthickness=1)
        
        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)
    
    def setup_button_hover_effects(self):
        """Setup hover effects for buttons"""
        def fetch_hover_enter(e):
            self.fetch_btn.config(bg=self.colors['text_primary'])
        
        def fetch_hover_leave(e):
            if self.fetch_btn['state'] != tk.DISABLED:
                self.fetch_btn.config(bg=self.colors['success'])
        
        def stop_hover_enter(e):
            if self.stop_btn['state'] != tk.DISABLED:
                self.stop_btn.config(bg=self.colors['text_primary'])
        
        def stop_hover_leave(e):
            if self.stop_btn['state'] != tk.DISABLED:
                self.stop_btn.config(bg=self.colors['danger'])
        
        self.fetch_btn.bind('<Enter>', fetch_hover_enter)
        self.fetch_btn.bind('<Leave>', fetch_hover_leave)
        self.stop_btn.bind('<Enter>', stop_hover_enter)
        self.stop_btn.bind('<Leave>', stop_hover_leave)
    
    def nav_hover_enter(self, button, frame):
        """Navigation hover enter effect"""
        if button.cget('bg') != self.colors['active']:
            button.config(bg=self.colors['hover'])
            frame.config(bg=self.colors['hover'])
    
    def nav_hover_leave(self, button, frame, is_active):
        """Navigation hover leave effect"""
        if is_active:
            button.config(bg=self.colors['active'])
            frame.config(bg=self.colors['active'])
        else:
            button.config(bg=self.colors['bg_sidebar'])
            frame.config(bg=self.colors['bg_sidebar'])
    
    def on_search_focus_in(self, event):
        """Handle search focus in"""
        if event.widget.get() == "Search matches...":
            event.widget.delete(0, tk.END)
            event.widget.config(fg=self.colors['text_primary'])
    
    def on_search_focus_out(self, event):
        """Handle search focus out"""
        if not event.widget.get():
            event.widget.insert(0, "Search matches...")
            event.widget.config(fg=self.colors['text_muted'])
    
    def smooth_scroll(self, event):
        """Smooth scrolling for canvas"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def start_live_animations(self):
        """Start background animations for live elements"""
        self.animate_live_indicator()
    
    def animate_live_indicator(self):
        """Animate live indicator in header"""
        if self.animation_active:
            current_color = self.live_dot.cget('fg')
            new_color = self.colors['bg_header'] if current_color == self.colors['live'] else self.colors['live']
            self.live_dot.config(fg=new_color)
            
        self.root.after(1000, self.animate_live_indicator)  # Blink every second
    
    def update_status(self, message, color, indicator="●"):
        """Update status with modern styling"""
        self.status_label.config(text=message, fg=color)
        self.status_dot.config(fg=color, text=indicator)
    
    # Core functionality methods
    def check_scraper_status(self):
        """Check if the scraper thread is still running"""
        if hasattr(self, 'scraper_thread') and self.scraper_thread.is_alive():
            self.root.after(100, self.check_scraper_status)
    
    def stop_fetching(self):
        """Stop the running scraper"""
        if hasattr(self, 'scraper') and self.scraper:
            self.scraper.stop()
        self.cleanup()
        self.update_status("Stopped by user", self.colors['warning'], "⏸")
        self.status_var.set("Operation stopped")
    
    def show_live_matches(self):
        """Show live matches"""
        self.update_nav_selection(0)  # First item in navigation
        self.content_title.config(text="Live Matches")
        self.content_subtitle.config(text="Real-time football scores and updates")
        self.status_var.set("Viewing live matches")
        
        # If we have data, process and display it
        if hasattr(self, 'scraper') and hasattr(self.scraper, 'json_data') and self.scraper.json_data:
            self.process_modern_results()
    
    def show_error(self, message):
        """Display an error message with modern styling"""
        messagebox.showerror("Error", message)
        self.cleanup()
        self.content_subtitle.config(text="Real-time football scores and updates")
        self.status_var.set("Viewing live matches")
    
    def show_fixtures(self):
        """Show upcoming fixtures"""
        self.update_nav_selection(1)
        self.content_title.config(text="Upcoming Fixtures")
        self.content_subtitle.config(text="Scheduled matches and kick-off times")
        self.status_var.set("Viewing upcoming fixtures")
    
    def show_favorites(self):
        """Show favorite matches"""
        self.update_nav_selection(2)
        self.content_title.config(text="Favorite Matches")
        self.content_subtitle.config(text="Your followed teams and matches")
        self.status_var.set("Viewing favorites")
    
    def show_settings(self):
        """Show settings"""
        self.update_nav_selection(3)
        self.content_title.config(text="Settings")
        self.content_subtitle.config(text="Customize your experience")
        self.status_var.set("Viewing settings")
    
    def update_nav_selection(self, active_index):
        """Update navigation selection styling"""
        for i, (btn, frame, _) in enumerate(self.nav_buttons):
            if i == active_index:
                btn.config(bg=self.colors['active'], fg=self.colors['primary'])
                frame.config(bg=self.colors['active'])
                self.nav_buttons[i] = (btn, frame, True)
            else:
                btn.config(bg=self.colors['bg_sidebar'], fg=self.colors['text_primary'])
                frame.config(bg=self.colors['bg_sidebar'])
                self.nav_buttons[i] = (btn, frame, False)


if __name__ == "__main__":
    root = tk.Tk()
    
    # Configure root window with modern styling
    root.configure(bg='#F8F9FA')
    
    # Set window icon (if available)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    app = FootballApp(root)
    root.mainloop()
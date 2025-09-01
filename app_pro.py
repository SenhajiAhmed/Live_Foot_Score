import tkinter as tk
from tkinter import ttk, messagebox
from scraper.match_scraper import MatchScraper
from datetime import datetime
import json
import threading

class FootballApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Football Scores Pro")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configure styles
        self.setup_styles()
        
        # Main container
        self.main_container = tk.Frame(root, bg='#f5f7fa')
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header()
        
        # Content area
        self.content_frame = tk.Frame(self.main_container, bg='#ffffff')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Left sidebar
        self.create_sidebar()
        
        # Right content
        self.create_content()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.main_container,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            style='Status.TLabel'
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_var.set("Ready")
        
        # Threading control
        self.is_running = False
    
    def setup_styles(self):
        """Configure application styles"""
        style = ttk.Style()
        
        # Configure colors
        self.colors = {
            'primary': '#1a237e',
            'primary_light': '#534bae',
            'secondary': '#00b0ff',
            'success': '#00c853',
            'warning': '#ffab00',
            'danger': '#ff1744',
            'dark': '#263238',
            'light': '#ffffff',
            'bg': '#f5f7fa',
            'border': '#e0e0e0',
            'text_primary': '#212121',
            'text_secondary': '#757575'
        }
        
        # Configure ttk styles
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('TLabel', background=self.colors['light'])
        style.configure('Status.TLabel', 
                       background=self.colors['primary'],
                       foreground='white',
                       padding=5)
    
    def create_header(self):
        """Create application header"""
        header = tk.Frame(
            self.main_container,
            bg=self.colors['primary'],
            height=60
        )
        header.pack(fill=tk.X)
        
        # App title
        title_frame = tk.Frame(header, bg=self.colors['primary'])
        title_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            title_frame,
            text="⚽",
            font=('Segoe UI', 24),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            title_frame,
            text="FOOTBALL SCORES",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT)
        
        # Current date
        self.date_var = tk.StringVar()
        self.date_var.set(datetime.now().strftime("%A, %B %d, %Y"))
        
        tk.Label(
            header,
            textvariable=self.date_var,
            font=('Segoe UI', 10),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.RIGHT, padx=20)
    
    def create_sidebar(self):
        """Create left sidebar with controls"""
        sidebar = tk.Frame(
            self.content_frame,
            bg='white',
            width=250,
            bd=1,
            relief=tk.SOLID
        )
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        sidebar.pack_propagate(False)
        
        # Search box
        search_frame = tk.Frame(sidebar, bg='white', padx=15, pady=15)
        search_frame.pack(fill=tk.X)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 10)
        )
        search_entry.pack(fill=tk.X, ipady=5)
        search_entry.insert(0, "Search matches...")
        
        # Navigation
        nav_frame = tk.Frame(sidebar, bg='white', pady=10)
        nav_frame.pack(fill=tk.X)
        
        nav_items = [
            ("📊 Live Matches", self.show_live_matches),
            ("📅 Fixtures", self.show_fixtures),
            ("⭐ Favorites", self.show_favorites),
            ("⚙️ Settings", self.show_settings)
        ]
        
        for text, command in nav_items:
            btn = tk.Button(
                nav_frame,
                text=text,
                font=('Segoe UI', 11),
                bg='white',
                fg=self.colors['text_primary'],
                bd=0,
                anchor='w',
                padx=20,
                pady=10,
                relief=tk.FLAT,
                command=command,
                cursor='hand2'
            )
            btn.pack(fill=tk.X)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.colors['bg']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='white'))
        
        # Divider
        ttk.Separator(sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Action buttons
        btn_frame = tk.Frame(sidebar, bg='white', padx=10, pady=10)
        btn_frame.pack(fill=tk.X)
        
        self.fetch_btn = ttk.Button(
            btn_frame,
            text="🔄 Fetch Matches",
            command=self.fetch_matches,
            style='Accent.TButton'
        )
        self.fetch_btn.pack(fill=tk.X, pady=(0, 5))
        
        self.stop_btn = ttk.Button(
            btn_frame,
            text="⏹ Stop",
            command=self.stop_fetching,
            state=tk.DISABLED,
            style='Danger.TButton'
        )
        self.stop_btn.pack(fill=tk.X)
        
        # Status
        self.status_label = tk.Label(
            sidebar,
            text="Ready to fetch matches",
            font=('Segoe UI', 9),
            fg=self.colors['success'],
            bg='white',
            anchor='w',
            padx=20,
            pady=10
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_content(self):
        """Create main content area"""
        content = tk.Frame(self.content_frame, bg='white')
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Content header
        header = tk.Frame(content, bg='white', height=60)
        header.pack(fill=tk.X, padx=20, pady=20)
        
        self.content_title = tk.Label(
            header,
            text="Live Matches",
            font=('Segoe UI', 18, 'bold'),
            fg=self.colors['dark'],
            bg='white',
            anchor='w'
        )
        self.content_title.pack(fill=tk.X)
        
        # Matches container
        self.matches_frame = tk.Frame(content, bg='white')
        self.matches_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Add a canvas and scrollbar
        self.canvas = tk.Canvas(
            self.matches_frame,
            bg='white',
            bd=0,
            highlightthickness=0
        )
        
        scrollbar = ttk.Scrollbar(
            self.matches_frame,
            orient=tk.VERTICAL,
            command=self.canvas.yview
        )
        
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the canvas and scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add mousewheel scrolling
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        )
        
        # Show empty state
        self.show_empty_state()
    
    def show_empty_state(self, message="No matches available"):
        """Show empty state in the content area"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        empty_frame = tk.Frame(self.scrollable_frame, bg='white', pady=50)
        empty_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(
            empty_frame,
            text="⚽",
            font=('Segoe UI', 48),
            fg=self.colors['border'],
            bg='white'
        ).pack(pady=(0, 20))
        
        tk.Label(
            empty_frame,
            text=message,
            font=('Segoe UI', 14),
            fg=self.colors['text_secondary'],
            bg='white'
        ).pack()
    
    def fetch_matches(self):
        """Start fetching matches in a separate thread"""
        if self.is_running:
            return
            
        self.is_running = True
        self.fetch_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(
            text="Fetching matches...",
            fg=self.colors['primary']
        )
        self.status_var.set("Fetching matches...")
        
        # Clear previous results
        self.show_empty_state("Fetching matches...")
        
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
    
    def run_scraper(self):
        """Run the scraper and process results"""
        try:
            success = self.scraper.run()
            if success:
                self.root.after(0, self.process_results)
            else:
                self.root.after(0, lambda: self.show_error("Failed to fetch matches. Please try again."))
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Error: {str(e)}"))
    
    def process_results(self):
        """Process and display the scraped results"""
        try:
            # Clear previous results
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            
            # Load the data from the JSON file
            try:
                with open('data/events.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except FileNotFoundError:
                self.show_empty_state("No match data available")
                return
                
            if 'events' in data and data['events']:
                # Group matches by tournament and status
                matches_by_tournament = {}
                
                for event in data['events']:
                    tournament_name = event['tournament']['name']
                    status_type = event['status']['type']
                    round_info = event.get('roundInfo', {})
                    round_name = round_info.get('round', 'Unknown Round')
                    
                    # Create a unique key for each tournament and round
                    key = f"{tournament_name} - {round_name}"
                    
                    if key not in matches_by_tournament:
                        matches_by_tournament[key] = {
                            'tournament': tournament_name,
                            'round': round_name,
                            'matches': []
                        }
                    
                    matches_by_tournament[key]['matches'].append(event)
                
                # Display only the first 3 tournaments
                displayed_tournaments = 0
                total_matches = 0
                
                for tournament_info in matches_by_tournament.values():
                    if displayed_tournaments >= 3:
                        break
                    self.display_tournament_matches(tournament_info)
                    displayed_tournaments += 1
                    total_matches += len(tournament_info['matches'])
                self.status_label.config(
                    text=f"Showing {total_matches} matches",
                    fg=self.colors['success']
                )
                self.status_var.set(f"Successfully loaded {total_matches} matches")
            else:
                self.show_empty_state("No matches available")
                self.status_label.config(
                    text="No matches found",
                    fg=self.colors['warning']
                )
                self.status_var.set("No matches found")
                
        except Exception as e:
            self.show_error(f"Error processing results: {str(e)}")
        finally:
            self.cleanup()
    
    def display_tournament_matches(self, tournament_info):
        """Display matches for a specific tournament in a horizontal layout"""
        # Create tournament header
        header_frame = tk.Frame(self.scrollable_frame, bg='white')
        header_frame.pack(fill=tk.X, pady=(15, 5), padx=10)
        
        tk.Label(
            header_frame,
            text=f"{tournament_info['tournament']} - {tournament_info['round']}",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['primary'],
            bg='white',
            anchor='w'
        ).pack(fill=tk.X)
        
        # Create a frame for the matches with horizontal scrolling
        matches_container = tk.Frame(self.scrollable_frame, bg='white')
        matches_container.pack(fill=tk.X, padx=10, pady=(0, 15))
        
        # Create a canvas for horizontal scrolling
        canvas = tk.Canvas(matches_container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(matches_container, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)
        
        canvas.pack(side="top", fill="x", expand=True)
        scrollbar.pack(side="bottom", fill="x")
        
        # Group matches by status
        matches_by_status = {}
        for match in tournament_info['matches']:
            status = match['status']['type']
            if status not in matches_by_status:
                matches_by_status[status] = []
            matches_by_status[status].append(match)
        
        # Display matches by status
        for status, matches in matches_by_status.items():
            status_frame = tk.Frame(scrollable_frame, bg='white')
            status_frame.pack(side=tk.LEFT, padx=5, fill=tk.Y)
            
            # Status header
            status_text = status.capitalize()
            if status == 'inprogress':
                status_text = 'LIVE '
            elif status == 'finished':
                status_text = 'FT '
                
            tk.Label(
                status_frame,
                text=status_text,
                font=('Segoe UI', 9, 'bold'),
                fg=self.colors['primary'],
                bg='white',
                bd=1,
                relief=tk.SOLID,
                padx=5,
                pady=2
            ).pack(fill=tk.X, pady=(0, 5))
            
            # Add matches for this status
            for match in matches:
                self.create_match_card_horizontal(match, status_frame)
    
    def create_match_card_horizontal(self, event, parent_frame):
        """Create a compact match card for horizontal display"""
        card = tk.Frame(
            parent_frame,
            bg='#f9f9f9',
            bd=1,
            relief=tk.SOLID,
            padx=10,
            pady=8,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        card.pack(side=tk.LEFT, fill=tk.Y, padx=3, pady=2)
        
        # Match status
        status_type = event['status']['type']
        is_live = status_type == 'inprogress'
        is_finished = status_type == 'finished'
        
        # Teams and scores
        home_team = event["homeTeam"]["name"]
        home_score = event["homeScore"].get("current", "-")
        away_team = event["awayTeam"]["name"]
        away_score = event["awayScore"].get("current", "-")
        
        # Home team
        home_frame = tk.Frame(card, bg='#f9f9f9')
        home_frame.pack(fill=tk.X, pady=1)
        
        tk.Label(
            home_frame,
            text=home_team[:15] + ('...' if len(home_team) > 15 else ''),
            font=('Segoe UI', 9),
            fg=self.colors['text_primary'],
            bg='#f9f9f9',
            anchor='w',
            width=15
        ).pack(side=tk.LEFT)
        
        # Status indicator
        status_frame = tk.Frame(card, bg='#f9f9f9')
        status_frame.pack(fill=tk.X, pady=2)
        
        # Score or time
        if is_finished:
            score_text = f"{home_score} - {away_score}"
            status_bg = '#e8f5e9'  # Light green for finished matches
            status_fg = '#2e7d32'
        elif is_live:
            minute = event.get('time', {}).get('minute', '')
            score_text = f"{home_score} - {away_score} {minute}'" if minute else f"{home_score} - {away_score}"
            status_bg = '#ffebee'  # Light red for live matches
            status_fg = '#c62828'
        else:
            try:
                match_time = datetime.fromtimestamp(event['startTimestamp']).strftime('%H:%M')
                score_text = match_time
            except:
                score_text = event['status']['description']
            status_bg = '#e3f2fd'  # Light blue for upcoming matches
            status_fg = '#1565c0'
        
        # Score/Time display
        score_label = tk.Label(
            status_frame,
            text=score_text,
            font=('Segoe UI', 9, 'bold'),
            fg=status_fg,
            bg=status_bg,
            bd=1,
            relief=tk.SOLID,
            padx=5,
            pady=1
        )
        score_label.pack()
        
        # Away team
        away_frame = tk.Frame(card, bg='#f9f9f9')
        away_frame.pack(fill=tk.X, pady=1)
        
        tk.Label(
            away_frame,
            text=away_team[:15] + ('...' if len(away_team) > 15 else ''),
            font=('Segoe UI', 9),
            fg=self.colors['text_primary'],
            bg='#f9f9f9',
            anchor='w',
            width=15
        ).pack(side=tk.LEFT)
        
        # Add winner indicator for finished matches
        if is_finished and 'winnerCode' in event['status']:
            winner_code = event['status']['winnerCode']
            if winner_code == 1:  # Home win
                home_frame.config(bg='#e8f5e9')
                home_frame.pack_configure(padx=2, pady=1)
                home_frame.pack_propagate(False)
                home_frame.config(width=120, height=20)
            elif winner_code == 2:  # Away win
                away_frame.config(bg='#e8f5e9')
                away_frame.pack_configure(padx=2, pady=1)
                away_frame.pack_propagate(False)
                away_frame.config(width=120, height=20)
            elif winner_code == 0:  # Draw
                status_frame.config(bg='#fff8e1')
                score_label.config(bg='#fff8e1', fg='#f57f17')
    
    def check_scraper_status(self):
        """Check if the scraper thread is still running"""
        if hasattr(self, 'scraper_thread') and self.scraper_thread.is_alive():
            self.root.after(100, self.check_scraper_status)
    
    def stop_fetching(self):
        """Stop the running scraper"""
        if hasattr(self, 'scraper') and self.scraper:
            self.scraper.stop()
        self.cleanup()
        self.status_label.config(
            text="Stopped by user",
            fg=self.colors['warning']
        )
        self.status_var.set("Operation stopped")
    
    def show_error(self, message):
        """Display an error message"""
        messagebox.showerror("Error", message)
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.is_running = False
        self.fetch_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    # Navigation methods
    def show_live_matches(self):
        """Show live matches"""
        self.content_title.config(text="Live Matches")
        self.status_var.set("Viewing live matches")
    
    def show_fixtures(self):
        """Show upcoming fixtures"""
        self.content_title.config(text="Upcoming Fixtures")
        self.status_var.set("Viewing upcoming fixtures")
    
    def show_favorites(self):
        """Show favorite matches"""
        self.content_title.config(text="Favorite Matches")
        self.status_var.set("Viewing favorites")
    
    def show_settings(self):
        """Show settings"""
        self.content_title.config(text="Settings")
        self.status_var.set("Viewing settings")


if __name__ == "__main__":
    root = tk.Tk()
    app = FootballApp(root)
    root.mainloop()

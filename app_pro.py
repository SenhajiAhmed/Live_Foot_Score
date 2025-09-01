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
            with open('data/events.json', 'r') as f:
                data = json.load(f)
                
            # Clear the content area
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
                
            if 'events' in data and data['events']:
                # Get only the first 5 matches
                matches_to_show = data['events'][:5]
                for event in matches_to_show:
                    self.create_match_card(event)
                self.status_label.config(
                    text=f"Showing {len(matches_to_show)} of {len(data['events'])} matches",
                    fg=self.colors['success']
                )
                self.status_var.set(f"Successfully loaded {len(matches_to_show)} matches")
            else:
                self.show_empty_state("No matches available for the selected date")
                self.status_label.config(
                    text="No matches found",
                    fg=self.colors['warning']
                )
                self.status_var.set("No matches found")
                
        except Exception as e:
            self.show_error(f"Error processing results: {str(e)}")
        finally:
            self.cleanup()
    
    def create_match_card(self, event):
        """Create a match card for display"""
        card = tk.Frame(
            self.scrollable_frame,
            bg='white',
            bd=1,
            relief=tk.SOLID,
            padx=15,
            pady=10,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        card.pack(fill=tk.X, pady=5)
        
        # Match status
        status_type = event['status']['type']
        is_live = status_type == 'inprogress'
        is_finished = status_type == 'finished'
        
        if is_finished:
            status_text = "FT"
            status_color = self.colors['text_secondary']
        elif is_live:
            status_text = f"LIVE {event.get('time', {}).get('minute', '')}'"
            status_color = self.colors['danger']
        else:
            try:
                match_time = datetime.fromtimestamp(event['startTimestamp']).strftime('%H:%M')
                status_text = match_time
                status_color = self.colors['text_secondary']
            except:
                status_text = event['status']['description']
                status_color = self.colors['text_secondary']
        
        # Status label
        status_frame = tk.Frame(card, bg='white')
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            status_frame,
            text=status_text,
            font=('Segoe UI', 10, 'bold'),
            fg=status_color,
            bg='white'
        ).pack(anchor='w')
        
        # Teams and scores
        home_team = event["homeTeam"]["name"]
        home_score = event["homeScore"].get("current", "-")
        away_team = event["awayTeam"]["name"]
        away_score = event["awayScore"].get("current", "-")
        
        # Home team
        home_frame = tk.Frame(card, bg='white')
        home_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(
            home_frame,
            text=home_team,
            font=('Segoe UI', 12),
            fg=self.colors['text_primary'],
            bg='white',
            anchor='w'
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            home_frame,
            text=str(home_score),
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['dark'],
            bg='white',
            width=3
        ).pack(side=tk.RIGHT)
        
        # Away team
        away_frame = tk.Frame(card, bg='white')
        away_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(
            away_frame,
            text=away_team,
            font=('Segoe UI', 12),
            fg=self.colors['text_primary'],
            bg='white',
            anchor='w'
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            away_frame,
            text=str(away_score),
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['dark'],
            bg='white',
            width=3
        ).pack(side=tk.RIGHT)
        
        # Competition info
        if 'tournament' in event and 'name' in event['tournament']:
            comp_frame = tk.Frame(card, bg='white')
            comp_frame.pack(fill=tk.X, pady=(10, 0))
            
            tk.Label(
                comp_frame,
                text=event['tournament']['name'],
                font=('Segoe UI', 9),
                fg=self.colors['text_secondary'],
                bg='white',
                anchor='w'
            ).pack(fill=tk.X)
    
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

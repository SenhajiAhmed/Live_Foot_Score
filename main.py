"""
Refactored Football Scores Pro Application
Main entry point that imports and orchestrates all components.
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.design_system import DesignSystem
from ui.header import Header
from ui.sidebar import Sidebar
from ui.content import ContentArea
from ui.status_bar import StatusBar
from ui.match_display import MatchDisplay
from data.data_processor import DataProcessor, MatchOrganizer


class FootballApp:
    """Main Football Scores Pro application."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Football Scores Pro")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Initialize design system
        self.design = DesignSystem()
        
        # Initialize data processor
        self.data_processor = DataProcessor()
        
        # Initialize match display
        self.match_display = MatchDisplay(self.design)
        
        # Setup main container
        self.setup_main_container()
        
        # Initialize UI components
        self.initialize_components()
        
        # Automatically fetch matches when the app starts
        self.root.after(1000, self.fetch_matches)
    
    def setup_main_container(self):
        """Setup the main container with gradient background"""
        self.main_container = tk.Frame(self.root, bg=self.design.colors['bg_primary'])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Content area with card design
        self.content_frame = tk.Frame(
            self.main_container, 
            bg=self.design.colors['bg_secondary'],
            relief=tk.FLAT
        )
        # Don't pack the content frame yet - it will be packed after the header
        self.content_frame.pack_propagate(False)
    
    def initialize_components(self):
        """Initialize all UI components"""
        # Create header first
        self.header = Header(self.main_container, self.design)
        
        # Now pack the content frame below the header
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create sidebar with callbacks
        sidebar_callbacks = {
            'fetch_matches': self.fetch_matches,
            'stop_fetching': self.stop_fetching,
            'show_live_matches': self.show_live_matches,
            'show_fixtures': self.show_fixtures,
            'show_favorites': self.show_favorites,
            'show_settings': self.show_settings
        }
        self.sidebar = Sidebar(self.content_frame, self.design, sidebar_callbacks)
        
        # Create content area
        self.content = ContentArea(self.content_frame, self.design)
        
        # Create status bar
        self.status_bar = StatusBar(self.main_container, self.design)
    
    def fetch_matches(self):
        """Start fetching matches with modern UI updates"""
        if self.data_processor.is_fetching():
            return
            
        # Update UI state
        self.sidebar.set_fetch_button_state(False)
        self.sidebar.update_status("Fetching matches...", self.design.colors['primary'], "●")
        self.status_bar.update_status("Fetching live matches...")
        
        # Show loading state
        self.content.show_modern_loading_state()
        
        # Start fetching with callback
        success = self.data_processor.start_fetching(self.on_data_fetched)
        
        if not success:
            error_msg = self.data_processor.get_last_error() or "Failed to start scraper"
            self.show_error(error_msg)
    
    def on_data_fetched(self, success, data_or_error):
        """Callback for when data fetching is complete"""
        if success:
            self.process_results(data_or_error)
        else:
            self.show_error(data_or_error)
    
    def process_results(self, data):
        """Process and display results with modern UI"""
        try:
            # Clear previous results
            self.content.clear_content()
            
            # Organize matches by tournament
            matches_by_tournament = MatchOrganizer.organize_matches_by_tournament(data)
            
            if matches_by_tournament:
                # Display all tournaments with modern styling
                total_matches = self.match_display.display_tournaments(
                    self.content.scrollable_frame, 
                    matches_by_tournament
                )
                
                # Get statistics
                stats = MatchOrganizer.get_match_statistics(matches_by_tournament)
                
                # Update status
                self.sidebar.update_status(f"Showing {total_matches} matches", self.design.colors['success'], "●")
                self.status_bar.update_status(f"Successfully loaded {total_matches} matches")
                self.status_bar.update_match_count(total_matches)
                
                print(f"Displayed {stats['total_tournaments']} tournaments with {total_matches} matches")
                print(f"Live: {stats['live_matches']}, Finished: {stats['finished_matches']}, Upcoming: {stats['upcoming_matches']}")
                
            else:
                self.content.show_modern_empty_state("No matches available")
                self.sidebar.update_status("No matches found", self.design.colors['warning'], "●")
                
        except Exception as e:
            self.show_error(f"Error processing results: {str(e)}")
        finally:
            self.cleanup()
    
    def stop_fetching(self):
        """Stop the running scraper"""
        self.data_processor.stop_fetching()
        self.cleanup()
        self.sidebar.update_status("Stopped by user", self.design.colors['warning'], "⏸")
        self.status_bar.update_status("Operation stopped")
    
    def cleanup(self):
        """Clean up after fetching is complete"""
        self.sidebar.set_fetch_button_state(True)
    
    def show_error(self, message):
        """Display an error message with modern styling"""
        messagebox.showerror("Error", message)
        self.cleanup()
        self.content.content_subtitle.config(text="Real-time football scores and updates")
        self.status_bar.update_status("Ready")
    
    def show_live_matches(self):
        """Show live matches"""
        self.sidebar.update_nav_selection(0)
        self.content.update_content_title("Live Matches", "Real-time football scores and updates")
        self.status_bar.update_status("Viewing live matches")
        
        # If we have data, process and display it
        data = self.data_processor.get_data()
        if data:
            self.process_results(data)
    
    def show_fixtures(self):
        """Show upcoming fixtures"""
        self.sidebar.update_nav_selection(1)
        self.content.update_content_title("Upcoming Fixtures", "Scheduled matches and kick-off times")
        self.status_bar.update_status("Viewing upcoming fixtures")
    
    def show_favorites(self):
        """Show favorite matches"""
        self.sidebar.update_nav_selection(2)
        self.content.update_content_title("Favorite Matches", "Your followed teams and matches")
        self.status_bar.update_status("Viewing favorites")
    
    def show_settings(self):
        """Show settings"""
        self.sidebar.update_nav_selection(3)
        self.content.update_content_title("Settings", "Customize your experience")
        self.status_bar.update_status("Viewing settings")


def main():
    """Main entry point for the application"""
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


if __name__ == "__main__":
    main()

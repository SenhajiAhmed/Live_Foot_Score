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
from core.theme_manager import ThemeManager
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
        
        try:
            # Initialize design system with saved theme or default to dark
            saved_theme = self.load_theme_preference()
            self.design = DesignSystem(theme=saved_theme or 'dark')
            
            # Initialize theme manager
            self.theme_manager = ThemeManager(self.design)
            
            # Initialize data processor
            self.data_processor = DataProcessor()
            
            # Initialize match display
            self.match_display = MatchDisplay(self.design)
            
            # Setup main container
            self.setup_main_container()
            
            # Initialize UI components
            self.initialize_components()
            
            # Register for theme changes
            self.design.register_theme_change_callback(self.on_theme_changed)
            
            # Apply initial theme
            self.apply_theme()
            
            # Automatically fetch matches when the app starts
            self.root.after(1000, self.fetch_matches)
            
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to initialize application: {str(e)}")
            self.root.destroy()
    
    def load_theme_preference(self):
        """Load theme preference from config file"""
        config_path = os.path.join(os.path.expanduser('~'), '.football_scores_pro', 'config.ini')
        if os.path.exists(config_path):
            try:
                import configparser
                config = configparser.ConfigParser()
                config.read(config_path)
                return config.get('App', 'theme', fallback='dark')
            except Exception:
                return 'dark'
        return 'dark'
    
    def save_theme_preference(self, theme):
        """Save theme preference to config file"""
        try:
            import configparser
            import os
            
            config_dir = os.path.join(os.path.expanduser('~'), '.football_scores_pro')
            os.makedirs(config_dir, exist_ok=True)
            
            config = configparser.ConfigParser()
            config['App'] = {'theme': theme}
            
            with open(os.path.join(config_dir, 'config.ini'), 'w') as f:
                config.write(f)
        except Exception as e:
            print(f"Failed to save theme preference: {e}")
    
    def on_theme_changed(self):
        """Handle theme change event"""
        self.save_theme_preference(self.design.current_theme)
        self.apply_theme()
    
    def apply_theme(self):
        """Apply current theme to the root window and main container"""
        try:
            # Update root and main container colors
            self.root.config(bg=self.design.colors['bg_primary'])
            self.main_container.config(bg=self.design.colors['bg_primary'])
            self.content_frame.config(bg=self.design.colors['bg_secondary'])
            
            # Update header if it exists
            if hasattr(self, 'header') and hasattr(self.header, 'update_theme'):
                self.header.update_theme(self.design)
                
            # Update sidebar if it exists
            if hasattr(self, 'sidebar') and hasattr(self.sidebar, 'refresh'):
                self.sidebar.refresh()
                
            # Update content area if it exists
            if hasattr(self, 'content') and hasattr(self.content, 'update_theme'):
                self.content.update_theme(self.design)
                
        except Exception as e:
            print(f"Error applying theme: {e}")
    
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
            'show_finished': self.show_finished,
            'show_settings': self.show_settings
        }
        self.sidebar = Sidebar(self.content_frame, self.design, sidebar_callbacks)
        
        # Create content area
        self.content = ContentArea(self.content_frame, self.design)
        
        # Set the match display and organizer components in content area
        self.content.set_match_display(self.match_display)
        self.content.set_match_organizer(MatchOrganizer)
        
        # Set theme callback for content area
        self.content.set_theme_callback(self.switch_theme)
        
        # Create status bar
        self.status_bar = StatusBar(self.main_container, self.design)
        
        # Register components with theme manager
        self.theme_manager.register_component(self.header)
        self.theme_manager.register_component(self.sidebar)
        self.theme_manager.register_component(self.content)
        self.theme_manager.register_component(self.status_bar)
        self.theme_manager.register_component(self.match_display)
    
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
            # Get statistics for status updates
            matches_by_tournament = MatchOrganizer.organize_matches_by_tournament(data)
            stats = MatchOrganizer.get_match_statistics(matches_by_tournament)
            
            # Update status with overall statistics
            self.sidebar.update_status(f"Loaded {stats['total_matches']} matches", self.design.colors['success'], "●")
            self.status_bar.update_status(f"Successfully loaded {stats['total_matches']} matches")
            self.status_bar.update_match_count(stats['total_matches'])
            
            print(f"Loaded {stats['total_tournaments']} tournaments with {stats['total_matches']} matches")
            print(f"Live: {stats['live_matches']}, Finished: {stats['finished_matches']}, Upcoming: {stats['upcoming_matches']}")
            
            # Display content based on current view
            if self.content.current_view == "live_matches":
                self.content.show_live_matches(data)
            elif self.content.current_view == "fixtures":
                self.content.show_fixtures(data)
            elif self.content.current_view == "finished":
                self.content.show_finished(data)
            else:
                # Default to live matches view
                self.content.show_live_matches(data)
                
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
        self.status_bar.update_status("Viewing live matches")
        
        # Get current data and show live matches
        data = self.data_processor.get_data()
        self.content.show_live_matches(data)
    
    def show_fixtures(self):
        """Show upcoming fixtures"""
        self.sidebar.update_nav_selection(1)
        self.status_bar.update_status("Viewing upcoming fixtures")
        
        # Get current data and show fixtures
        data = self.data_processor.get_data()
        self.content.show_fixtures(data)
    
    def show_finished(self):
        """Show finished matches"""
        self.sidebar.update_nav_selection(2)
        self.status_bar.update_status("Viewing finished matches")
        
        # Get current data and show finished matches
        data = self.data_processor.get_data()
        self.content.show_finished(data)
    
    def show_settings(self):
        """Show settings"""
        self.sidebar.update_nav_selection(3)
        self.status_bar.update_status("Viewing settings")
        
        # Show settings view
        self.content.show_settings()
    
    def switch_theme(self, theme):
        """Switch application theme"""
        if self.theme_manager.switch_theme(theme):
            # Update root window background
            self.root.configure(bg=self.design.colors['bg_primary'])
            
            # Update main container background
            self.main_container.configure(bg=self.design.colors['bg_primary'])
            
            # Update content frame background
            self.content_frame.configure(bg=self.design.colors['bg_secondary'])
            
            print(f"Theme switched to: {theme}")
            self.status_bar.update_status(f"Switched to {theme} theme")
        else:
            print(f"Failed to switch to theme: {theme}")


def main():
    """Main entry point for the application"""
    root = tk.Tk()
    
    # Configure root window with modern styling
    # Will be updated by the design system based on theme
    root.configure(bg='#1A1A1A')  # Start with dark theme
    
    # Set window icon (if available)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    app = FootballApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

"""
Data Processing Module
Handles data processing, scraper integration, and match data organization.
"""

import json
import os
import threading
from scraper.match_scraper import MatchScraper


class DataProcessor:
    """Handles data processing and scraper integration."""
    
    def __init__(self, output_path=None):
        self.output_path = output_path or os.path.join("data", "events.json")
        self.scraper = None
        self.scraper_thread = None
        self.is_running = False
        self.json_data = None
        self.last_error = None
        self.max_initial_matches = 50  # Limit initial matches to prevent UI freezing
        self.cache_duration = 300  # Cache data for 5 minutes
        self.last_fetch_time = 0
        self.cached_data = None
    
    def start_fetching(self, callback=None):
        """Start fetching matches in a separate thread"""
        if self.is_running:
            return False
            
        self.is_running = True
        self.last_error = None
        
        try:
            # Initialize the scraper
            self.scraper = MatchScraper(output_path=self.output_path)
            
            # Run the scraper in a separate thread
            self.scraper_thread = threading.Thread(target=self._run_scraper, args=(callback,))
            self.scraper_thread.daemon = True
            self.scraper_thread.start()
            
            return True
        except Exception as e:
            self.last_error = str(e)
            self.is_running = False
            return False
    
    def _run_scraper(self, callback=None):
        """Run the scraper and process results"""
        try:
            # Run the scraper
            success = self.scraper.run()
            
            if success and hasattr(self.scraper, 'json_data') and self.scraper.json_data:
                self.json_data = self.scraper.json_data
                if callback:
                    callback(True, self.json_data)
            else:
                error_msg = "Failed to fetch matches. Please check your internet connection and try again."
                if hasattr(self.scraper, 'last_error'):
                    error_msg = f"Error: {self.scraper.last_error}"
                self.last_error = error_msg
                if callback:
                    callback(False, error_msg)
        except Exception as e:
            error_msg = f"An unexpected error occurred: {str(e)}"
            self.last_error = error_msg
            if callback:
                callback(False, error_msg)
        finally:
            self.is_running = False
    
    def stop_fetching(self):
        """Stop the running scraper"""
        if self.scraper:
            self.scraper.stop()
        self.is_running = False
    
    def load_data_from_file(self):
        """Load data from the JSON file"""
        try:
            with open(self.output_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except Exception as e:
            self.last_error = f"Error loading data: {str(e)}"
            return None
    
    def get_data(self):
        """Get the current data (from memory or file)"""
        if self.json_data:
            return self.json_data
        
        return self.load_data_from_file()
    
    def is_fetching(self):
        """Check if currently fetching data"""
        return self.is_running
    
    def get_last_error(self):
        """Get the last error message"""
        return self.last_error
    
    def get_limited_data(self, max_matches=None):
        """Get limited data for initial display to prevent UI freezing"""
        if max_matches is None:
            max_matches = self.max_initial_matches
            
        data = self.get_data()
        if not data or 'events' not in data:
            return data
            
        # Sort events by priority (live first, then by timestamp)
        events = data['events']
        
        # Separate by status
        live_events = [e for e in events if e.get('status', {}).get('type') == 'inprogress']
        finished_events = [e for e in events if e.get('status', {}).get('type') == 'finished']
        upcoming_events = [e for e in events if e.get('status', {}).get('type') not in ['inprogress', 'finished']]
        
        # Sort by timestamp (most recent first for finished, earliest first for upcoming)
        finished_events.sort(key=lambda x: x.get('startTimestamp', 0), reverse=True)
        upcoming_events.sort(key=lambda x: x.get('startTimestamp', 0))
        
        # Combine with priority: live first, then recent finished, then upcoming
        limited_events = live_events + finished_events[:max_matches//2] + upcoming_events[:max_matches//2]
        
        # Limit total matches
        limited_events = limited_events[:max_matches]
        
        return {
            'events': limited_events,
            'total_available': len(events),
            'showing': len(limited_events)
        }
    
    def is_cache_valid(self):
        """Check if cached data is still valid"""
        import time
        return (self.cached_data is not None and 
                time.time() - self.last_fetch_time < self.cache_duration)
    
    def get_cached_data(self):
        """Get cached data if valid"""
        if self.is_cache_valid():
            return self.cached_data
        return None
    
    def set_cached_data(self, data):
        """Cache data with timestamp"""
        import time
        self.cached_data = data
        self.last_fetch_time = time.time()
    
    def clear_cache(self):
        """Clear cached data"""
        self.cached_data = None
        self.last_fetch_time = 0


class MatchOrganizer:
    """Organizes match data by tournament and status."""
    
    @staticmethod
    def organize_matches_by_tournament(data):
        """Organize matches by tournament"""
        if not data or 'events' not in data or not data['events']:
            return {}
        
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
        
        return matches_by_tournament
    
    @staticmethod
    def get_match_statistics(matches_by_tournament):
        """Get statistics about the matches"""
        total_matches = 0
        total_tournaments = len(matches_by_tournament)
        
        live_count = 0
        finished_count = 0
        upcoming_count = 0
        
        for tournament_info in matches_by_tournament.values():
            for match in tournament_info['matches']:
                total_matches += 1
                status = match['status']['type']
                if status == 'inprogress':
                    live_count += 1
                elif status == 'finished':
                    finished_count += 1
                else:
                    upcoming_count += 1
        
        return {
            'total_matches': total_matches,
            'total_tournaments': total_tournaments,
            'live_matches': live_count,
            'finished_matches': finished_count,
            'upcoming_matches': upcoming_count
        }

import json
from datetime import datetime

class MatchFormatter:
    def __init__(self, input_path="data/events.json", output_path="data/foot_results.txt"):
        self.input_path = input_path
        self.output_path = output_path

    def format_and_save(self):
        with open(self.input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        output_lines = []
        
        # Group matches by tournament and round
        matches_by_tournament = {}
        
        for event in data.get("events", []):
            tournament_name = event['tournament']['name']
            round_info = event.get('roundInfo', {})
            round_name = round_info.get('round', 'N/A')
            
            # Create a unique key for each tournament and round combination
            key = f"{tournament_name} - {round_name}"
            
            if key not in matches_by_tournament:
                matches_by_tournament[key] = {
                    'tournament': tournament_name,
                    'round': round_name,
                    'season': event['season']['name'],
                    'matches': []
                }
            
            # Add match to the appropriate group
            home = event["homeTeam"]["name"]
            away = event["awayTeam"]["name"]
            home_score = event["homeScore"].get("current", "N/A")
            away_score = event["awayScore"].get("current", "N/A")
            
            match_info = {
                'home': home,
                'away': away,
                'home_score': home_score,
                'away_score': away_score,
                'status': event['status'],
                'start_timestamp': event.get('startTimestamp')
            }
            
            matches_by_tournament[key]['matches'].append(match_info)
        
        # Format the output
        for key, group in matches_by_tournament.items():
            # Tournament header
            output_lines.append(f"🏆 {group['tournament']} - {group['season']}")
            output_lines.append(f"🌀 Round: {group['round']}")
            output_lines.append("")
            
            # Group matches by status (e.g., inprogress, finished, notstarted)
            matches_by_status = {}
            for match in group['matches']:
                status = match['status']['type']
                if status not in matches_by_status:
                    matches_by_status[status] = []
                matches_by_status[status].append(match)
            
            # Display matches by status
            for status, matches in matches_by_status.items():
                status_display = status.capitalize()
                if status == 'inprogress':
                    status_display = 'Live 🔴'
                elif status == 'finished':
                    status_display = 'FT ✅'
                
                output_lines.append(f"📊 {status_display} Matches:")
                
                # Format matches horizontally with consistent width
                max_line_length = 100  # Maximum characters per line
                current_line = []
                current_line_length = 0
                
                for match in matches:
                    # Format the match entry
                    home = match['home']
                    away = match['away']
                    home_score = match['home_score']
                    away_score = match['away_score']
                    
                    # Base match string
                    if home_score != "N/A" and away_score != "N/A":
                        score_line = f"{home} {home_score}-{away_score} {away}"
                    else:
                        # If match hasn't started, show time
                        time_str = ""
                        if match['start_timestamp']:
                            dt = datetime.utcfromtimestamp(match['start_timestamp']).strftime('%H:%M')
                            time_str = f" ({dt})"
                        score_line = f"{home} vs {away}{time_str}"
                    
                    # Add status indicators
                    if status == 'inprogress':
                        score_line = f"🟢 {score_line}"
                    elif status == 'finished':
                        if 'winnerCode' in match['status']:
                            code = match['status']['winnerCode']
                            if code == 1:
                                score_line = f"🏆 {score_line}"
                            elif code == 2:
                                score_line = f"{score_line} 🏆"
                            elif code == 0:
                                score_line = f"{score_line} (D)"
                    else:  # not started
                        score_line = f"⏳ {score_line}"
                    
                    # Add some padding for better readability
                    match_display = f" {score_line} "
                    match_length = len(match_display)
                    
                    # If adding this match would exceed the line length, start a new line
                    if current_line and current_line_length + match_length + 3 > max_line_length:  # +3 for the ' | ' separator
                        output_lines.append(" | ".join(current_line))
                        current_line = []
                        current_line_length = 0
                    
                    current_line.append(match_display)
                    current_line_length += match_length + (3 if current_line_length > 0 else 0)  # Add separator length if not first item
                
                # Add any remaining matches in the current line
                if current_line:
                    output_lines.append(" | ".join(current_line))
                
                output_lines.append("")  # Add empty line between status groups
            
            output_lines.append("=" * 70)  # Add separator between tournaments
            output_lines.append("")  # Add empty line between tournament groups

        # Save to file
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))

        print(f"📝 Results saved to: {self.output_path}")

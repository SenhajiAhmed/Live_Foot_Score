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

        for event in data.get("events", []):
            tournament_line = f"🏆 Tournament: {event['tournament']['name']}"
            season_line = f"🗓️ Season: {event['season']['name']}"
            round_line = f"🌀 Round: {event.get('roundInfo', {}).get('round', 'N/A')}"
            status_line = f"📊 Status: {event['status']['description']} ({event['status']['type']})"

            home = event["homeTeam"]["name"]
            away = event["awayTeam"]["name"]
            home_score = event["homeScore"].get("current", "N/A")
            away_score = event["awayScore"].get("current", "N/A")

            match_line = f"⚽ Match: {home} vs {away}"
            if home_score != "N/A" and away_score != "N/A":
                score_line = f"🔢 Score: {home} {home_score} - {away_score} {away}"
            else:
                score_line = f"🔢 Score: Not available (match {event['status']['type']})"

            time_line = ""
            if timestamp := event.get("startTimestamp"):
                dt = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')
                time_line = f"⏰ Start time: {dt}"

            winner_line = ""
            if event["status"]["type"] == "finished" and "winnerCode" in event:
                code = event["winnerCode"]
                if code == 1:
                    winner_line = f"🏅 Winner: {home}"
                elif code == 2:
                    winner_line = f"🏅 Winner: {away}"
                else:
                    winner_line = "🏅 Result: Draw"

            # Append all to output
            output_lines += [
                tournament_line,
                season_line,
                round_line,
                status_line,
                match_line,
                score_line,
            ]
            if time_line:
                output_lines.append(time_line)
            if winner_line:
                output_lines.append(winner_line)

            output_lines += ["-" * 50, ""]

        # Save to file
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))

        print(f"📝 Results saved to: {self.output_path}")

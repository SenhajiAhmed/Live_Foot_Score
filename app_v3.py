import flet as ft
import json
import threading
from datetime import datetime
import time
# from scraper.match_scraper import MatchScraper  # Uncomment when available


class ModernFootballApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.is_running = False
        self.progress_ring = None
        self.status_text = None
        self.matches_container = None
        self.setup_page()
        self.build_ui()

    # ------------------------------------------------------------------
    # Page setup
    # ------------------------------------------------------------------
    def setup_page(self):
        """Configure the main page settings"""
        self.page.title = "⚽ Football Score Viewer"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.spacing = 0
        self.page.bgcolor = ft.Colors.GREY_50
        self.page.window_width = 1000
        self.page.window_height = 800
        self.page.window_center = True

        # Custom theme colors
        self.page.theme = ft.Theme(
            color_scheme_seed=ft.Colors.BLUE_600,
            visual_density=ft.VisualDensity.COMFORTABLE
        )

    # ------------------------------------------------------------------
    # UI building helpers
    # ------------------------------------------------------------------
    def build_ui(self):
        """Build the complete user interface"""
        main_container = ft.Container(
            content=ft.Column([
                self.create_header(),
                self.create_controls(),
                self.create_status_section(),
                self.create_results_section(),
                self.create_footer()
            ], spacing=0, tight=True),
            gradient=ft.LinearGradient(
                colors=[ft.Colors.BLUE_50, ft.Colors.INDIGO_50],
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center
            ),
            expand=True
        )
        self.page.add(main_container)

    # ------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------
    def create_header(self):
        return ft.Container(
            content=ft.Column([
                ft.Container(height=30),  # Top spacing
                ft.Row([
                    ft.Icon(ft.Icons.SPORTS_SOCCER, size=50, color=ft.Colors.WHITE),
                    ft.Column([
                        ft.Text(
                            "Football Score Viewer",
                            size=36,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE
                        ),
                        ft.Text(
                            "Live match statistics and scores",
                            size=16,
                            color=ft.Colors.WHITE70,
                            italic=True
                        )
                    ], spacing=0)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                ft.Container(height=30)  # Bottom spacing
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            gradient=ft.LinearGradient(
                colors=[ft.Colors.BLUE_600, ft.Colors.PURPLE_600],
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right
            ),
            border_radius=ft.border_radius.only(bottom_left=20, bottom_right=20)
        )

    # ------------------------------------------------------------------
    # Controls
    # ------------------------------------------------------------------
    def create_controls(self):
        self.fetch_btn = ft.ElevatedButton(
            text="Get Live Scores",
            icon=ft.Icons.SPORTS_SOCCER,
            on_click=self.fetch_scores,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_600,
                elevation=8,
                padding=ft.padding.symmetric(horizontal=30, vertical=15),
                shape=ft.RoundedRectangleBorder(radius=15),
                animation_duration=200
            ),
            width=200,
            height=50
        )

        self.stop_btn = ft.ElevatedButton(
            text="Stop",
            icon=ft.Icons.STOP,
            on_click=self.stop_scraping,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.RED_600,
                elevation=8,
                padding=ft.padding.symmetric(horizontal=25, vertical=15),
                shape=ft.RoundedRectangleBorder(radius=15)
            ),
            width=120,
            height=50,
            disabled=True
        )

        clear_btn = ft.ElevatedButton(
            text="Clear",
            icon=ft.Icons.CLEAR,
            on_click=self.clear_results,
            style=ft.ButtonStyle(
                color=ft.Colors.GREY_700,
                bgcolor=ft.Colors.GREY_200,
                elevation=4,
                padding=ft.padding.symmetric(horizontal=25, vertical=15),
                shape=ft.RoundedRectangleBorder(radius=15)
            ),
            width=120,
            height=50
        )

        return ft.Container(
            content=ft.Row([
                self.fetch_btn,
                self.stop_btn,
                clear_btn
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
            padding=ft.padding.symmetric(vertical=25)
        )

    # ------------------------------------------------------------------
    # Status section
    # ------------------------------------------------------------------
    def create_status_section(self):
        self.status_text = ft.Text(
            "Ready to fetch match data",
            size=16,
            color=ft.Colors.GREEN_600,
            weight=ft.FontWeight.W_500  # FIXED: W500 -> W_500
        )

        self.progress_ring = ft.ProgressRing(
            width=30,
            height=30,
            stroke_width=3,
            color=ft.Colors.BLUE_600,
            visible=False
        )

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    self.progress_ring,
                    self.status_text
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=10)
        )

    # ------------------------------------------------------------------
    # Results section
    # ------------------------------------------------------------------
    def create_results_section(self):
        results_header = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.ASSESSMENT, color=ft.Colors.BLUE_700),
                ft.Text(
                    "Match Results",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700
                )
            ], spacing=10),
            padding=ft.padding.symmetric(horizontal=20, vertical=15)
        )

        self.matches_container = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=15,
            height=400,
            auto_scroll=True
        )

        matches_wrapper = ft.Container(
            content=self.matches_container,
            padding=ft.padding.all(20),
            expand=True
        )

        return ft.Container(
            content=ft.Column([
                results_header,
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                matches_wrapper
            ], spacing=0),
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            margin=ft.margin.symmetric(horizontal=20),
            elevation=4,
            expand=True
        )

    # ------------------------------------------------------------------
    # Footer
    # ------------------------------------------------------------------
    def create_footer(self):
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, color=ft.Colors.AMBER_600, size=16),
                ft.Text(
                    "Tip: Data is fetched in real-time and shows the latest 5 matches",
                    size=12,
                    color=ft.Colors.GREY_600
                )
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            padding=ft.padding.symmetric(vertical=15)
        )

    # ------------------------------------------------------------------
    # Match card
    # ------------------------------------------------------------------
    def create_match_card(self, event, match_num):
        tournament = event["tournament"]["name"]
        season = event["season"]["name"]
        status_txt = event["status"]["description"]
        status_typ = event["status"]["type"]

        home_team = event["homeTeam"]["name"]
        away_team = event["awayTeam"]["name"]
        home_score = event["homeScore"].get("current", "—")
        away_score = event["awayScore"].get("current", "—")

        start_ts = event.get("startTimestamp")
        date_str = (
            datetime.utcfromtimestamp(start_ts).strftime("%d %b %Y • %H:%M UTC")
            if start_ts else "TBD"
        )

        # Determine status color and icon
        if status_typ == "finished":
            status_color = ft.Colors.GREEN_600
            status_icon = ft.Icons.CHECK_CIRCLE
        elif status_typ == "inprogress":
            status_color = ft.Colors.RED_600
            status_icon = ft.Icons.RADIO_BUTTON_CHECKED
        else:
            status_color = ft.Colors.ORANGE_600
            status_icon = ft.Icons.SCHEDULE

        # Determine winner styling
        home_winner = False
        away_winner = False
        if home_score != "—" and away_score != "—":
            try:
                if int(home_score) > int(away_score):
                    home_winner = True
                elif int(away_score) > int(home_score):
                    away_winner = True
            except (ValueError, TypeError):
                pass  # Handle non-numeric scores

        card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Text(
                                tournament,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_700
                            ),
                            ft.Text(
                                f"{season} • {date_str}",
                                size=12,
                                color=ft.Colors.GREY_600
                            )
                        ], expand=True, spacing=2),
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(status_icon, color=status_color, size=16),
                                ft.Text(status_txt, color=status_color, weight=ft.FontWeight.W_500)
                            ], spacing=5),
                            bgcolor="#e8f4fd",
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            border_radius=12
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                    ft.Divider(height=1, color=ft.Colors.GREY_200),

                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.HOME, size=16, color=ft.Colors.BLUE_600),
                                    ft.Text("HOME", size=10, color=ft.Colors.GREY_500)
                                ], spacing=4),
                                ft.Text(
                                    home_team,
                                    size=14,
                                    weight=ft.FontWeight.BOLD if home_winner else ft.FontWeight.NORMAL,
                                    color=ft.Colors.GREEN_700 if home_winner else ft.Colors.GREY_800
                                )
                            ], spacing=4),
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Row([
                                ft.Text(
                                    str(home_score),
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.GREEN_700 if home_winner else ft.Colors.GREY_800
                                ),
                                ft.Text(
                                    ":",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.GREY_400
                                ),
                                ft.Text(
                                    str(away_score),
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.GREEN_700 if away_winner else ft.Colors.GREY_800
                                )
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                            width=100
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text("AWAY", size=10, color=ft.Colors.GREY_500),
                                    ft.Icon(ft.Icons.FLIGHT, size=16, color=ft.Colors.ORANGE_600)
                                ], spacing=4, alignment=ft.MainAxisAlignment.END),
                                ft.Text(
                                    away_team,
                                    size=14,
                                    weight=ft.FontWeight.BOLD if away_winner else ft.FontWeight.NORMAL,
                                    color=ft.Colors.GREEN_700 if away_winner else ft.Colors.GREY_800,
                                    text_align=ft.TextAlign.RIGHT
                                )
                            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.END),
                            expand=True
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                    ft.Container(
                        content=ft.Row([
                            ft.Icon(
                                ft.Icons.EMOJI_EVENTS if (home_winner or away_winner) else ft.Icons.HANDSHAKE,
                                color=ft.Colors.AMBER_600,
                                size=16
                            ),
                            ft.Text(
                                f"{home_team} wins!" if home_winner else
                                f"{away_team} wins!" if away_winner else
                                "Draw" if (home_score != "—" and away_score != "—" and home_score == away_score) else
                                f"Match {status_txt.lower()}",
                                size=12,
                                color=ft.Colors.AMBER_700,
                                weight=ft.FontWeight.W_500  # FIXED: W500 -> W_500
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                        bgcolor=ft.Colors.AMBER_50,
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=15,
                        margin=ft.margin.only(top=10)
                    )
                ], spacing=12),
                padding=ft.padding.all(20)
            ),
            elevation=4,
            surface_tint_color=ft.Colors.BLUE_50,
            margin=ft.margin.symmetric(vertical=5)
        )

        return card

    # ------------------------------------------------------------------
    # Status helpers
    # ------------------------------------------------------------------
    def update_status(self, message, is_loading=False):
        self.status_text.value = message
        self.progress_ring.visible = is_loading
        self.page.update()

    def clear_results(self, e):
        self.matches_container.controls.clear()
        self.update_status("Results cleared")

    def stop_scraping(self, e):
        self.is_running = False
        self.update_status("Stopping...", False)

    # ------------------------------------------------------------------
    # Main fetch logic (runs in thread)
    # ------------------------------------------------------------------
    def fetch_scores(self, e):
        def run_task():
            try:
                self.is_running = True
                self.fetch_btn.disabled = True
                self.stop_btn.disabled = False
                self.page.update()

                self.update_status("🔄 Initializing scraper...", True)
                self.matches_container.controls.clear()
                self.page.update()

                loading_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.ProgressRing(width=50, height=50),
                            ft.Text("🚀 Starting football data scraper...",
                                    size=16, text_align=ft.TextAlign.CENTER)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                        padding=ft.padding.all(30)
                    ),
                    elevation=2
                )
                self.matches_container.controls.append(loading_card)
                self.page.update()

                if not self.is_running:
                    return

                self.update_status("📡 Fetching live match data...", True)
                # Note: Uncomment the next two lines when you have the scraper module
                # scraper = MatchScraper()
                # scraper.run()

                if not self.is_running:
                    return

                self.update_status("📂 Loading match data...", True)

                try:
                    with open("data/events.json", "r", encoding="utf-8") as f:
                        data = json.load(f)
                except FileNotFoundError:
                    data = {
                        "events": [
                            {
                                "tournament": {"name": "Premier League"},
                                "season": {"name": "2024/25"},
                                "status": {"description": "Finished", "type": "finished"},
                                "homeTeam": {"name": "Manchester United"},
                                "awayTeam": {"name": "Liverpool"},
                                "homeScore": {"current": 2},
                                "awayScore": {"current": 1},
                                "startTimestamp": int(datetime.now().timestamp())
                            },
                            {
                                "tournament": {"name": "La Liga"},
                                "season": {"name": "2024/25"},
                                "status": {"description": "In Progress", "type": "inprogress"},
                                "homeTeam": {"name": "Barcelona"},
                                "awayTeam": {"name": "Real Madrid"},
                                "homeScore": {"current": 1},
                                "awayScore": {"current": 1},
                                "startTimestamp": int(datetime.now().timestamp())
                            }
                        ]
                    }

                if not self.is_running:
                    return

                events = data.get("events", [])[:5]

                self.matches_container.controls.clear()

                if not events:
                    no_data_card = ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.SEARCH_OFF, size=50, color=ft.Colors.GREY_400),
                                ft.Text("⚠️ No matches found in the data.",
                                        size=16, color=ft.Colors.GREY_600)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                            padding=ft.padding.all(30)
                        )
                    )
                    self.matches_container.controls.append(no_data_card)
                    self.update_status("No matches available")
                    return

                self.update_status("🎯 Displaying results...", True)

                for idx, event in enumerate(events, 1):
                    if not self.is_running:
                        break
                    match_card = self.create_match_card(event, idx)
                    self.matches_container.controls.append(match_card)
                    self.page.update()
                    time.sleep(0.1)

                if self.is_running:
                    success_message = ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_600),
                            ft.Text(f"✅ Successfully loaded {len(events)} matches!",
                                    color=ft.Colors.GREEN_600, weight=ft.FontWeight.W_500)
                        ], spacing=8),
                        bgcolor=ft.Colors.GREEN_50,
                        padding=ft.padding.all(15),
                        border_radius=10,
                        margin=ft.margin.symmetric(vertical=10)
                    )
                    self.matches_container.controls.append(success_message)
                    self.update_status(f"✅ Loaded {len(events)} matches successfully")

            except FileNotFoundError:
                self.update_status("❌ Data file not found - Using demo data")
                error_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.INFO, size=50, color=ft.Colors.BLUE_400),
                            ft.Text("Using demo data - Connect your scraper for live data",
                                    size=16, color=ft.Colors.BLUE_600)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                        padding=ft.padding.all(30)
                    )
                )
                self.matches_container.controls.clear()
                self.matches_container.controls.append(error_card)
                self.page.update()
            except json.JSONDecodeError:
                self.update_status("❌ Invalid data format")
            except Exception as ex:
                self.update_status(f"❌ Error: {str(ex)}")
            finally:
                self.is_running = False
                self.fetch_btn.disabled = False
                self.stop_btn.disabled = True
                self.update_status("Ready to fetch match data")
                self.page.update()

        threading.Thread(target=run_task, daemon=True).start()


# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------
def main(page: ft.Page):
    app = ModernFootballApp(page)


if __name__ == "__main__":
    ft.app(target=main)
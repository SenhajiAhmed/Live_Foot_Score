# Football Scores Pro

A Python application that displays live and upcoming football matches with a clean, modern UI. The app fetches match data from various sources and presents it in an easy-to-read format.

## Features

- 🏆 View matches from top football leagues
- ⚽ Live scores and match updates
- 📅 Upcoming fixtures with match times
- 🎨 Clean, modern user interface
- 🔄 Automatic data refresh
- 📱 Responsive design

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SenhajiAhmed/football-scores-pro.git
   cd football-scores-pro
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Playwright browsers:
   ```bash
   playwright install
   ```

5. Install Playwright system dependencies (if needed):
   ```bash
   playwright install-deps
   ```

## Usage

1. Run the application:
   ```bash
   python app_pro.py
   ```

2. The application will start and display the main window with live and upcoming matches.

3. Use the sidebar to navigate between different views:
   - 📊 Live Matches
   - 📅 Fixtures
   - ⭐ Favorites
   - ⚙️ Settings

## Project Structure

- `app_pro.py` - Main application file
- `scraper/` - Contains web scraping utilities
  - `match_scraper.py` - Handles fetching match data
  - `match_formatter.py` - Formats match data for display
- `data/` - Directory for storing match data
- `requirements.txt` - Python dependencies

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## Screenshots

*Screenshots will be added soon*

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

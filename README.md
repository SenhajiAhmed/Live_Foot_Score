# Football Scores Pro

A modern Python application that displays live and upcoming football matches with a clean, responsive UI. The app fetches match data from various sources and presents it in an easy-to-read format.

## ✨ Features

- 🏆 View matches from top football leagues worldwide
- ⚽ Live scores with real-time updates
- 📅 Upcoming fixtures with match times in your local timezone
- 🎨 Sleek, modern user interface with dark/light themes
- 🔄 Automatic data refresh to keep scores current
- 📱 Responsive design that works on all screen sizes
- 📊 Tournament organization and match grouping
- ⚡ Optimized performance with threaded data fetching

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Playwright (for web scraping)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SenhajiAhmed/Live_Foot_Score.git
   cd Live_Foot_Score
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Playwright**:
   ```bash
   playwright install
   playwright install-deps  # Install system dependencies if needed
   ```

## 🏃‍♂️ Running the Application

You can start the application using:

```bash

python main.py

```

## 🎮 User Interface

The application features an intuitive interface with several key components:

- **Header**: Shows the app logo, live indicator, and current date
- **Sidebar**: Navigation menu with search functionality
- **Main Content**: Displays matches organized by tournament
- **Status Bar**: Shows the current status and match count

## 🏗️ Project Structure

```
football-scores/
├── app_pro.py           # Original application entry point
├── main.py              # Refactored application entry point
├── src/                 # Source code
│   ├── core/            # Core functionality
│   │   └── design_system.py  # Design tokens and theming
│   ├── ui/              # User interface components
│   │   ├── header.py    # Header component
│   │   ├── sidebar.py   # Navigation sidebar
│   │   ├── content.py   # Main content area
│   │   └── ...         # Other UI components
│   ├── data/            # Data processing
│   └── utils/           # Utility functions
├── scraper/             # Web scraping utilities
│   ├── match_scraper.py # Match data fetching
│   └── match_formatter.py
└── data/                # Local data storage
    └── events.json
```

## 🔧 Technical Details

### Key Components

1. **Data Processing**
   - Threaded data fetching for responsive UI
   - Smart caching to minimize API calls
   - Error handling and retry mechanisms

2. **User Interface**
   - Modern, responsive design
   - Smooth animations and transitions
   - Theme support (light/dark mode)

3. **Testing**
   - `test_imports.py`: Verifies all modules can be imported correctly
     - Validates design system initialization
     - Checks UI component imports
     - Tests data processing modules
     - Provides clear success/error feedback
   - Run tests with: `python test_imports.py`

4. **Performance**
   - Optimized rendering
   - Efficient data updates
   - Minimal resource usage

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For questions or support, please open an issue on the [GitHub repository](https://github.com/SenhajiAhmed/Live_Foot_Score/issues).

---

*Screenshots will be added soon*

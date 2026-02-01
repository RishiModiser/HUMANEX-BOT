# HUMANEX Version 5 - Traffic Simulation Bot

A professional traffic simulation bot with Direct Visit mode, featuring a PyQt5 GUI and Playwright browser automation for human-like website interaction.

## Features

### Direct Visit Mode
- **Professional GUI**: Built with PyQt5 for a clean and intuitive user interface
- **Browser Automation**: Uses Playwright for reliable and realistic browser control
- **Human-like Scrolling**: 
  - Randomized scroll intervals (0.5-2.5 seconds between scrolls)
  - Variable scroll distances (50-300 pixels per scroll)
  - Smooth scrolling animations with varying speeds
  - Random reading pauses to simulate natural user behavior
- **Non-headless Mode**: Browser runs visibly for live monitoring
- **Detailed Logging**: Comprehensive logs of all actions including:
  - Browser initialization
  - Page navigation
  - Scroll actions with details
  - Session completion
  - Error handling

## Requirements

- Python 3.7 or higher
- PyQt5
- Playwright

## Installation

1. Clone the repository:
```bash
git clone https://github.com/RishiModiser/HUMANEX-BOT.git
cd HUMANEX-BOT
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

## Usage

### Running the Application

```bash
python humanex_bot.py
```

### Using the Direct Visit Mode

1. Launch the application using the command above
2. Enter the target website URL in the input field (e.g., `https://example.com`)
3. Click the "Start Simulation" button
4. The browser will open automatically and begin the simulation
5. Monitor the activity log for detailed information about each action
6. The browser will close automatically when the simulation completes

### Example URLs to Test

- `https://example.com` - Simple test website
- `https://github.com` - GitHub homepage
- `https://wikipedia.org` - Wikipedia main page

## How It Works

### Human-like Scrolling Algorithm

The bot simulates realistic human scrolling behavior through:

1. **Variable Scroll Distance**: Each scroll moves between 50-300 pixels, mimicking how humans don't scroll uniformly
2. **Randomized Timing**: Waits 0.5-2.5 seconds between scrolls, similar to natural reading speed
3. **Reading Pauses**: 20% chance of longer pauses (2-5 seconds) to simulate detailed reading
4. **Smooth Animation**: Uses browser's smooth scroll behavior for natural movement
5. **Initial and Final Pauses**: Includes delays before starting and after completing to simulate page loading review

### Architecture

- **Main Thread**: Handles the GUI and user interactions
- **Worker Thread**: Manages browser automation without blocking the UI
- **Signal/Slot Communication**: Enables thread-safe logging and status updates

## Logging

All actions are logged with timestamps in the following format:
```
[2026-02-01 20:15:30] Initializing browser automation...
[2026-02-01 20:15:31] Launching browser in non-headless mode...
[2026-02-01 20:15:32] Opening new page...
[2026-02-01 20:15:33] Navigating to URL: https://example.com
[2026-02-01 20:15:35] Successfully loaded: https://example.com
[2026-02-01 20:15:38] Starting human-like scrolling simulation...
[2026-02-01 20:15:39] Scroll #1: 150px in 0.75s (waiting 1.23s)
...
```

## Future Enhancements

This implementation provides the foundation for:
- Additional traffic modes (Search Engine Mode, Social Media Mode, etc.)
- Advanced interaction settings (form filling, button clicking, etc.)
- RPA script execution capabilities
- Multi-session management
- Analytics and reporting
- Proxy support
- Custom user agent rotation

## Troubleshooting

### Browser Not Opening
- Ensure Playwright browsers are installed: `playwright install chromium`
- Check that you have sufficient system resources

### URL Not Loading
- Verify the URL is correct and includes `http://` or `https://`
- Check your internet connection
- Some websites may block automation - try different sites

### Application Not Starting
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version is 3.7 or higher: `python --version`

## License

This project is open source and available for educational and research purposes.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Author

RishiModiser

## Version

5.0.0 - Direct Visit Mode

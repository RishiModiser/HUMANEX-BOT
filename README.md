# HUMANEX Version 5 - Advanced Traffic Simulation Bot

A professional, feature-rich traffic simulation bot with advanced fingerprinting, proxy support, multiple traffic modes, human-like interactions, and an RPA system. Built with PyQt5 GUI and Playwright browser automation.

## 🌟 Key Features

### Traffic Simulation Modes
- **Direct Visit Mode**: Direct URL visits with human-like scrolling and interactions
- **Search Traffic Mode**: Automated Google search with target website detection and clicking
- **Referral Traffic Mode**: Generate authentic UTM-tracked links simulating social media, paid social, and other referral sources

### Advanced Capabilities
- **10,000+ User Agents**: Latest Android and Windows user agents for advanced fingerprinting
- **Proxy Support**: Multiple proxy formats with automatic rotation
  - `ip:port`
  - `ip:port:username:password`
  - `username:password@ip:port`
  - `http://ip:port`
  - `http://username:password@ip:port`
  - `socks5://ip:port`
  - `socks5://username:password@ip:port`
- **Concurrent Profiles**: Run up to 200 simultaneous browser profiles
- **Platform Selection**: Choose Windows, Android, or Random platform
- **Adjustable Stay Times**: Configure how long to interact with pages (10-600 seconds)
- **Non-Headless Mode**: All browser interactions are visible for monitoring

### Human-Like Interactions
- **Advanced Scrolling**: Randomized scroll distances, intervals, and reading pauses
- **Article Clicking**: Intelligently finds and clicks on article links
- **Text Highlighting**: Simulates user reading by highlighting random text
- **Extra Pages**: Opens additional pages based on configured limits
- **Mouse Movements**: Realistic cursor movements across pages

### RPA System
- **Visual Script Creator**: Drag-and-drop style interface for creating automation scripts
- **Supported Actions**:
  - Navigate to URL
  - Click elements
  - Input text
  - Scroll page
  - Wait/pause
  - Select dropdown options
  - Hover over elements
- **JSON Import/Export**: Save and load RPA scripts
- **Script Execution**: Run custom RPA scripts during traffic simulation

### Elite GUI
- **Professional Dark Theme**: Modern, aesthetically pleasing interface
- **Real-Time Logging**: Comprehensive activity logs with timestamps
- **Progress Tracking**: Visual progress bar for simulation status
- **Statistics Display**: Live stats including available user agents
- **Multiple Panels**: Organized controls and log viewing

## 📋 Requirements

- Python 3.7 or higher
- PyQt5
- Playwright
- Internet connection

## 🚀 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/RishiModiser/HUMANEX-BOT.git
cd HUMANEX-BOT
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install Playwright browsers:**
```bash
playwright install chromium
```

## 💻 Usage

### Running HUMANEX Version 5

```bash
python humanex_v5.py
```

### Quick Start Guide

1. **Launch the application**
2. **Configure Basic Settings:**
   - Enter target URL (e.g., `https://example.com`)
   - Select traffic mode (Direct, Search, or Referral)
   - For Search mode, enter a search query

3. **Configure Advanced Settings:**
   - Choose platform (Windows/Android/Random)
   - Set stay time (seconds to spend on page)
   - Set number of extra pages to visit
   - Set concurrent profiles (1-200)

4. **Optional - Configure Proxies:**
   - Enter proxies in the text area (one per line)
   - Click "Load Proxies"
   - Supported formats listed in Features section

5. **Optional - Create/Load RPA Script:**
   - Click "Create RPA Script" to build custom automation
   - Or click "Load RPA Script" to import existing JSON
   - Script will execute after main traffic simulation

6. **Start Simulation:**
   - Click "START SIMULATION"
   - Monitor activity log for detailed progress
   - Click "STOP" to halt simulation if needed

### Running Legacy Version (Direct Visit Only)

```bash
python humanex_bot.py
```

### Running CLI Demo

```bash
python demo.py https://example.com
```

## 🎯 Traffic Modes Explained

### Direct Visit Mode
Simulates a user directly typing a URL and visiting a website:
- Navigates directly to target URL
- Performs human-like scrolling
- Highlights text randomly
- Clicks on articles/links
- Opens extra pages if configured

### Search Traffic Mode
Simulates a user finding your site through search engines:
- Searches on Google with your query
- Finds your domain in search results
- Clicks on your site's link
- Performs all Direct Visit interactions
- Falls back to direct visit if site not found in results

### Referral Traffic Mode
Simulates traffic from social media and other referral sources:
- Generates authentic UTM parameters
  - `utm_source`: facebook, twitter, instagram, etc.
  - `utm_medium`: social, paid_social, email, etc.
  - `utm_campaign`: Custom campaign identifiers
- Optionally visits referrer site first
- Navigates to your site with tracking parameters
- Performs all Direct Visit interactions

## 🤖 RPA Script System

### Creating RPA Scripts

1. Click "Create RPA Script" button
2. Enter script name and description
3. Select action type from dropdown
4. Fill in action parameters
5. Click "Add Action" to add to script
6. Repeat for all desired actions
7. Preview JSON in real-time
8. Click "Export JSON" to save script
9. Click "OK" to use script in simulation

### Action Types

| Action | Parameters | Description |
|--------|-----------|-------------|
| Navigate | URL | Navigate to a specific URL |
| Click | Selector | Click on an element |
| Input | Selector, Text | Type text into input field |
| Scroll | Direction, Amount | Scroll page up or down |
| Wait | Seconds | Pause execution |
| Select | Selector, Value | Select dropdown option |
| Hover | Selector | Hover mouse over element |

### Example RPA Script

```json
{
  "name": "Login Example",
  "description": "Automated login flow",
  "actions": [
    {
      "type": "navigate",
      "params": {"url": "https://example.com/login"}
    },
    {
      "type": "input",
      "params": {"selector": "#username", "text": "user@example.com"}
    },
    {
      "type": "input",
      "params": {"selector": "#password", "text": "password123"}
    },
    {
      "type": "click",
      "params": {"selector": "#login-button"}
    },
    {
      "type": "wait",
      "params": {"seconds": 3}
    }
  ]
}
```

## 🔧 Advanced Configuration

### Proxy Configuration

Proxies are automatically rotated for each concurrent profile. To maximize effectiveness:

1. Use high-quality, dedicated proxies
2. Mix proxy locations for geographic diversity
3. Test proxies before use
4. Monitor for proxy failures in logs

### Concurrent Profiles

Running multiple concurrent profiles:
- **1-10 profiles**: Safe for most systems
- **11-50 profiles**: Requires good CPU and RAM
- **51-200 profiles**: Requires powerful system with adequate resources

**Note**: Each profile opens a visible browser window, so excessive profiles may overwhelm your display and system resources.

### Platform Selection

- **Windows**: Uses Windows 10/11 user agents with Chrome, Edge, Firefox
- **Android**: Uses Android 10-14 user agents with Chrome, Samsung Browser
- **Random**: Randomly selects between Windows and Android for each profile

## 📊 Statistics & Monitoring

### Activity Log
Real-time logging includes:
- Browser initialization
- Page navigation
- Traffic mode execution
- Interaction details (scrolling, clicking, text highlighting)
- RPA script execution
- Errors and warnings
- Session completion

### Export Logs
Click "Export Log" to save activity logs to a text file for analysis.

## 🎨 GUI Features

### Professional Dark Theme
- Modern, eye-friendly dark interface
- Blue accent colors for visual hierarchy
- Clear section grouping
- Responsive controls

### Layout
- **Left Panel**: All configuration controls
- **Right Panel**: Real-time activity log
- **Bottom**: Status bar with current status

## 🛠️ Technical Architecture

### Modules

| Module | Purpose |
|--------|---------|
| `humanex_v5.py` | Main application with GUI |
| `user_agents.py` | 10,000+ user agent database |
| `proxy_handler.py` | Proxy parsing and rotation |
| `traffic_modes.py` | Traffic mode implementations |
| `interactions.py` | Human-like interaction engine |
| `rpa_system.py` | RPA script system |

### Threading Model
- **Main Thread**: GUI and user interactions
- **Worker Threads**: Browser automation (one per concurrent profile)
- **Signal/Slot**: Thread-safe communication

## ⚠️ Important Notes

### System Resources
- Each concurrent profile uses significant CPU and RAM
- Visible browser windows use additional GPU resources
- Monitor system performance when running many profiles

### Website Compatibility
- Some websites have bot detection mechanisms
- Advanced sites may block automation attempts
- Use proxies and vary user agents to improve success rates
- Not all sites support automated interaction

### Legal & Ethical Use
- Only use on websites you own or have permission to test
- Respect robots.txt and website terms of service
- Do not use for malicious purposes or DDoS attacks
- Use responsibly for legitimate testing and analytics

### Proxy Considerations
- Free proxies are often unreliable
- Use reputable proxy providers
- Rotating residential proxies work best
- Some websites block known proxy IPs

## 🐛 Troubleshooting

### Browser Not Opening
- Ensure Playwright browsers are installed: `playwright install chromium`
- Check system resources (CPU, RAM)
- Try reducing concurrent profiles

### Timeout Errors
- Increase stay time for slower connections
- Check internet connectivity
- Verify target URL is accessible
- Some sites may have rate limiting

### Proxy Errors
- Verify proxy format is correct
- Test proxies individually
- Check proxy authentication credentials
- Some proxies may be blocked by target site

### High CPU/Memory Usage
- Reduce concurrent profiles
- Close other applications
- Increase stay time to reduce churning
- Use more powerful hardware

### RPA Script Failures
- Verify selectors are correct
- Use browser DevTools to find accurate selectors
- Add Wait actions between steps
- Test scripts on stable websites first

## 📈 Future Enhancements

Potential features for future versions:
- Click-through rate optimization
- Session recording and playback
- Advanced analytics dashboard
- Headless mode option (optional)
- Custom fingerprint profiles
- Browser cache and cookie management
- Multi-account management
- Scheduled automation
- API integration
- Cloud deployment support

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available for educational and research purposes.

## 👤 Author

**RishiModiser**

## 🌐 Repository

https://github.com/RishiModiser/HUMANEX-BOT

## 📦 Version History

### Version 5.0.0 (Current)
- Complete rewrite with advanced features
- Multiple traffic modes (Direct, Search, Referral)
- 10,000+ user agents
- Proxy support with multiple formats
- Concurrent profiles (up to 200)
- RPA script system
- Elite GUI design
- Advanced human-like interactions

### Version 4.0.0
- Basic direct visit mode
- Simple human-like scrolling
- PyQt5 GUI
- Single browser automation

## 💡 Tips for Best Results

1. **Start Small**: Begin with 1-2 profiles to test configuration
2. **Use Quality Proxies**: Invest in good residential proxies
3. **Vary Settings**: Use different platforms, stay times, and traffic modes
4. **Monitor Logs**: Watch for errors and adjust accordingly
5. **Test RPA Scripts**: Verify scripts work before production use
6. **Respect Limits**: Don't overwhelm target websites
7. **Stay Updated**: Keep Playwright and dependencies updated

## 📞 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Check existing issues for solutions
- Review troubleshooting section
- Consult Playwright documentation

## ⚡ Performance Tips

- **SSD Storage**: Faster disk I/O for browser operations
- **High RAM**: At least 8GB for 10+ profiles, 16GB+ for more
- **Multi-Core CPU**: More cores = better concurrent performance
- **Stable Internet**: High-bandwidth connection for multiple profiles
- **Optimize OS**: Close unnecessary background applications

---

**HUMANEX Version 5** - Professional Traffic Simulation for Modern Web Testing

*Built with ❤️ for the automation community*

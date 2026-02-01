# HUMANEX Version 5 - Quick Start Guide

## Getting Started in 5 Minutes

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (required for automation)
playwright install chromium
```

### 2. Launch HUMANEX V5

```bash
python humanex_v5.py
```

### 3. Basic Usage - Direct Visit

**Simplest way to start:**

1. The application opens with default settings
2. Target URL is pre-filled: `https://example.com`
3. Click **START SIMULATION**
4. Watch the browser open and simulate human interaction
5. Monitor the activity log on the right

**That's it!** You've just run your first traffic simulation.

---

## Common Use Cases

### Use Case 1: Simple Website Traffic

**Goal:** Generate basic traffic to your website

**Steps:**
1. Enter your website URL
2. Keep "Direct Visit" mode selected
3. Set stay time: 180 seconds (3 minutes)
4. Keep concurrent profiles at 1
5. Click START SIMULATION

**Result:** One browser will visit your site for 3 minutes with human-like behavior.

---

### Use Case 2: Search Engine Traffic

**Goal:** Simulate users finding your site through Google

**Steps:**
1. Enter your website URL: `https://yoursite.com`
2. Select "Search Traffic" mode
3. Enter search query: `your business keywords`
4. Set stay time: 180 seconds
5. Click START SIMULATION

**Result:** Browser searches Google, finds your site, clicks it, then interacts naturally.

---

### Use Case 3: Social Media Referral Traffic

**Goal:** Simulate traffic from social media platforms

**Steps:**
1. Enter your website URL
2. Select "Referral Traffic" mode
3. Set stay time: 180 seconds
4. Click START SIMULATION

**Result:** Visit includes UTM tracking parameters simulating Facebook, Twitter, Instagram, etc.

---

### Use Case 4: Multiple Concurrent Visitors

**Goal:** Simulate multiple users visiting simultaneously

**Steps:**
1. Enter your website URL
2. Select traffic mode
3. Set "Concurrent Profiles": 5 (or any number 1-200)
4. Set stay time: 120 seconds
5. Click START SIMULATION

**Result:** 5 browsers open simultaneously, each simulating a different user.

**Warning:** Each profile uses significant resources. Start with 1-5, then scale up.

---

### Use Case 5: Using Proxies

**Goal:** Visit from different IP addresses

**Steps:**
1. In "Proxy Configuration" section, enter proxies (one per line):
   ```
   192.168.1.1:8080
   user:pass@192.168.1.2:8080
   http://192.168.1.3:8080
   ```
2. Click "Load Proxies"
3. Verify count shows loaded proxies
4. Configure other settings
5. Click START SIMULATION

**Result:** Each concurrent profile uses a different proxy from your list.

---

### Use Case 6: Platform-Specific Traffic

**Goal:** Simulate mobile or desktop traffic

**Steps:**
1. In "Advanced Settings", select Platform:
   - **Windows**: Desktop browser simulation
   - **Android**: Mobile browser simulation  
   - **Random**: Mix of both
2. Configure other settings
3. Click START SIMULATION

**Result:** Browser uses appropriate user agent for selected platform.

---

### Use Case 7: Deep Engagement (Extra Pages)

**Goal:** Simulate users exploring multiple pages

**Steps:**
1. Enter your website URL
2. Set "Extra Pages": 3
3. Set stay time: 300 seconds (5 minutes)
4. Click START SIMULATION

**Result:** Bot visits main page, then clicks and visits 3 additional pages/articles.

---

### Use Case 8: Creating RPA Scripts

**Goal:** Automate custom actions (login, form fill, etc.)

**Steps:**
1. Click "Create RPA Script"
2. Enter script name: "Login Test"
3. Add actions:
   - Navigate: `https://yoursite.com/login`
   - Input: Selector `#username`, Text `user@example.com`
   - Input: Selector `#password`, Text `password123`
   - Click: Selector `#login-button`
   - Wait: 3 seconds
4. Click "Export JSON" to save (optional)
5. Click OK to use in simulation
6. Start simulation

**Result:** Bot performs your custom automation sequence after main traffic simulation.

---

## Understanding the Interface

### Left Panel (Controls)

**Basic Configuration:**
- **Target URL**: Website to visit
- **Traffic Mode**: How to reach the site
- **Search Query**: For search traffic mode

**Advanced Settings:**
- **Platform**: Windows/Android/Random
- **Stay Time**: Seconds on site (10-600)
- **Extra Pages**: Additional pages to visit (0-10)
- **Concurrent Profiles**: Simultaneous browsers (1-200)

**Proxy Configuration:**
- Enter proxies, one per line
- Multiple formats supported
- Load/Clear buttons

**RPA Script:**
- Create custom automation
- Load existing scripts
- Optional feature

**Controls:**
- **START SIMULATION**: Begin automation
- **STOP**: Halt all running profiles
- **Progress Bar**: Visual status

### Right Panel (Logging)

**Activity Log:**
- Real-time updates
- Timestamped events
- Error messages
- Clear/Export buttons

---

## Tips for Best Results

### Starting Out
1. **Start with 1 profile** - Test your configuration first
2. **Use short stay times** - 60-120 seconds for testing
3. **Watch the log** - Learn what's happening
4. **Try example.com first** - Simple, reliable test site

### Scaling Up
1. **Gradually increase profiles** - 1 → 3 → 5 → 10
2. **Monitor system resources** - CPU, RAM, GPU usage
3. **Use proxies for large scale** - Avoid rate limiting
4. **Increase stay times** - More realistic engagement

### Troubleshooting
1. **Browser doesn't open?** 
   - Run: `playwright install chromium`
   - Check system resources

2. **Timeout errors?**
   - Increase stay time
   - Check internet connection
   - Try different website

3. **High CPU/Memory?**
   - Reduce concurrent profiles
   - Close other applications
   - Increase stay time

4. **Proxy not working?**
   - Verify format
   - Test proxy independently
   - Check authentication

---

## Example Configurations

### Configuration 1: Quick Test
- URL: `https://example.com`
- Mode: Direct Visit
- Platform: Random
- Stay Time: 60 seconds
- Profiles: 1
- Proxies: None

**Use:** Quick functionality test

---

### Configuration 2: Realistic Traffic
- URL: `https://yoursite.com`
- Mode: Search Traffic
- Query: `your product name`
- Platform: Random
- Stay Time: 180 seconds
- Extra Pages: 2
- Profiles: 3
- Proxies: 5 quality proxies

**Use:** Realistic multi-user engagement

---

### Configuration 3: Social Media Campaign
- URL: `https://yoursite.com/landing`
- Mode: Referral Traffic
- Platform: Android
- Stay Time: 120 seconds
- Extra Pages: 1
- Profiles: 10
- Proxies: 15 mobile proxies

**Use:** Simulate social media campaign traffic

---

### Configuration 4: Load Testing
- URL: `https://yoursite.com`
- Mode: Direct Visit
- Platform: Random
- Stay Time: 300 seconds
- Extra Pages: 3
- Profiles: 50
- Proxies: 100 proxies

**Use:** Stress testing (requires powerful system)

---

## Command Line Alternatives

### Legacy Version (Simple)
```bash
python humanex_bot.py
```
Opens simplified GUI with Direct Visit only.

### CLI Demo (No GUI)
```bash
python demo.py https://example.com
```
Runs single Direct Visit session from command line.

---

## Safety & Best Practices

### Do's ✓
- Test on websites you own
- Start with low profile counts
- Monitor system resources
- Use quality proxies for scale
- Respect website rate limits
- Export logs for analysis

### Don'ts ✗
- Don't target websites without permission
- Don't overwhelm servers with excessive traffic
- Don't use for malicious purposes
- Don't ignore error messages
- Don't run 200 profiles on weak hardware
- Don't use free/unreliable proxies for production

---

## Support

**Issues or Questions?**
- Check README.md for detailed documentation
- Review this guide for common scenarios
- Check GitHub Issues for known problems
- Open new issue with details if needed

**Success Stories?**
- Share your use cases
- Contribute improvements
- Help others learn

---

## Next Steps

1. **Run your first test** - Use Configuration 1 above
2. **Experiment with modes** - Try Direct, Search, Referral
3. **Create RPA script** - Automate custom actions
4. **Scale gradually** - Increase profiles slowly
5. **Monitor and optimize** - Watch logs, adjust settings

---

**HUMANEX Version 5** - Professional traffic simulation made simple!

*Happy automating! 🚀*

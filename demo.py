#!/usr/bin/env python3
"""
Simple command-line version for testing the bot without GUI
This is useful for testing or automation scenarios
"""

import sys
import time
from playwright.sync_api import sync_playwright
import random
from datetime import datetime


# Constants
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


def log(message):
    """Print log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def human_like_scroll(page):
    """Simulate human-like scrolling behavior
    
    Args:
        page: Playwright page object representing the browser page to scroll
    """
    log("Starting human-like scrolling simulation...")
    
    # Get page height
    page_height = page.evaluate("document.body.scrollHeight")
    viewport_height = page.evaluate("window.innerHeight")
    
    current_position = 0
    scroll_count = 0
    
    while current_position < page_height - viewport_height:
        # Randomize scroll distance (50-300 pixels)
        scroll_distance = random.randint(50, 300)
        
        # Randomize scroll speed
        scroll_duration = random.uniform(0.3, 1.2)
        
        # Calculate new position
        new_position = min(current_position + scroll_distance, page_height - viewport_height)
        
        # Perform smooth scroll
        page.evaluate(f"""
            window.scrollTo({{
                top: {new_position},
                behavior: 'smooth'
            }});
        """)
        
        scroll_count += 1
        current_position = new_position
        
        # Randomize interval between scrolls
        scroll_interval = random.uniform(0.5, 2.5)
        log(f"Scroll #{scroll_count}: {scroll_distance}px in {scroll_duration:.2f}s (waiting {scroll_interval:.2f}s)")
        
        time.sleep(scroll_interval)
        
        # Sometimes pause for a longer duration
        if random.random() < 0.2:  # 20% chance
            reading_pause = random.uniform(2.0, 5.0)
            log(f"Simulating reading pause: {reading_pause:.2f}s")
            time.sleep(reading_pause)
    
    log(f"Scrolling completed. Total scrolls: {scroll_count}")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python demo.py <URL>")
        print("Example: python demo.py https://example.com")
        sys.exit(1)
    
    url = sys.argv[1]
    
    if not url.startswith(('http://', 'https://')):
        print("ERROR: URL must start with http:// or https://")
        sys.exit(1)
    
    log("="*80)
    log("HUMANEX Bot - Direct Visit Mode (CLI Demo)")
    log(f"Target URL: {url}")
    log("="*80)
    
    try:
        log("Initializing browser automation...")
        
        with sync_playwright() as p:
            log("Launching browser in non-headless mode...")
            browser = p.chromium.launch(headless=False)
            
            log("Creating new browser context...")
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent=USER_AGENT
            )
            
            log("Opening new page...")
            page = context.new_page()
            
            log(f"Navigating to URL: {url}")
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            log(f"Successfully loaded: {url}")
            
            # Initial pause
            initial_pause = random.uniform(2.0, 4.0)
            log(f"Initial pause before scrolling: {initial_pause:.2f}s")
            time.sleep(initial_pause)
            
            # Perform human-like scrolling
            human_like_scroll(page)
            
            # Final pause
            final_pause = random.uniform(3.0, 6.0)
            log(f"Final pause before closing: {final_pause:.2f}s")
            time.sleep(final_pause)
            
            log("Closing browser...")
            context.close()
            browser.close()
            
            log("Session completed successfully!")
            log("="*80)
            
    except Exception as e:
        log(f"ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

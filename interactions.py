"""
HUMANEX Version 5 - Advanced Interactions
Human-like interactions including scrolling, clicking, and text highlighting
"""

import random
import time


class InteractionEngine:
    """Engine for human-like interactions"""
    
    def __init__(self, page, logger=None):
        self.page = page
        self.logger = logger
    
    def log(self, message):
        """Log a message"""
        if self.logger:
            self.logger(message)
    
    def human_like_scroll(self, duration=None):
        """
        Simulate human-like scrolling behavior
        
        Args:
            duration: Optional total duration in seconds (if None, scroll entire page)
        """
        self.log("Starting human-like scrolling...")
        
        try:
            # Get page dimensions
            page_height = self.page.evaluate("document.body.scrollHeight")
            viewport_height = self.page.evaluate("window.innerHeight")
            
            current_position = 0
            scroll_count = 0
            start_time = time.time()
            
            while current_position < page_height - viewport_height:
                # Check duration limit
                if duration and (time.time() - start_time) > duration:
                    break
                
                # Randomize scroll distance (50-300 pixels)
                scroll_distance = random.randint(50, 300)
                
                # Calculate new position
                new_position = min(current_position + scroll_distance, page_height - viewport_height)
                
                # Perform smooth scroll
                self.page.evaluate(f"""
                    window.scrollTo({{
                        top: {new_position},
                        behavior: 'smooth'
                    }});
                """)
                
                scroll_count += 1
                current_position = new_position
                
                # Randomize interval between scrolls (0.5-2.5 seconds)
                scroll_interval = random.uniform(0.5, 2.5)
                time.sleep(scroll_interval)
                
                # Sometimes pause for longer (simulate reading)
                if random.random() < 0.2:  # 20% chance
                    reading_pause = random.uniform(2.0, 5.0)
                    self.log(f"Reading pause: {reading_pause:.2f}s")
                    time.sleep(reading_pause)
            
            self.log(f"Scrolling completed. Total scrolls: {scroll_count}")
            
        except Exception as e:
            self.log(f"Scroll error: {str(e)}")
    
    def click_random_article(self, max_attempts=5):
        """
        Click on a random article/link on the page
        
        Args:
            max_attempts: Maximum number of attempts to find clickable element
            
        Returns:
            bool: True if successfully clicked, False otherwise
        """
        self.log("Looking for random article to click...")
        
        try:
            # Find all clickable links
            links = self.page.query_selector_all('a')
            
            if not links:
                self.log("No links found on page")
                return False
            
            # Filter out external links and navigation (keep article-like links)
            article_links = []
            current_domain = self.page.url.split('/')[2]
            
            for link in links:
                href = link.get_attribute('href')
                if href and (href.startswith('/') or current_domain in href):
                    # Check if link has visible text
                    text = link.inner_text().strip()
                    if text and len(text) > 10:  # Article links usually have descriptive text
                        article_links.append(link)
            
            if not article_links:
                self.log("No suitable article links found")
                return False
            
            # Select random article link
            target_link = random.choice(article_links)
            link_text = target_link.inner_text().strip()[:50]  # First 50 chars
            
            self.log(f"Clicking article: {link_text}...")
            
            # Scroll to element first (more human-like)
            target_link.scroll_into_view_if_needed()
            time.sleep(random.uniform(0.5, 1.5))
            
            # Click the link
            target_link.click()
            
            # Wait for navigation
            self.page.wait_for_load_state('networkidle', timeout=30000)
            
            self.log(f"Successfully clicked and loaded new page")
            return True
            
        except Exception as e:
            self.log(f"Click article error: {str(e)}")
            return False
    
    def highlight_random_text(self, num_highlights=None):
        """
        Highlight random text on the page (simulates user reading/selecting)
        
        Args:
            num_highlights: Number of text selections to make (random if None)
        """
        if num_highlights is None:
            num_highlights = random.randint(2, 5)
        
        self.log(f"Highlighting random text ({num_highlights} selections)...")
        
        try:
            for i in range(num_highlights):
                # Get all text nodes
                paragraphs = self.page.query_selector_all('p')
                
                if not paragraphs:
                    break
                
                # Select random paragraph
                para = random.choice(paragraphs)
                
                # Scroll to paragraph
                para.scroll_into_view_if_needed()
                time.sleep(random.uniform(0.5, 1.0))
                
                # Select text (simulate triple-click or drag selection)
                try:
                    para.click(click_count=3)  # Triple-click selects paragraph
                    time.sleep(random.uniform(1.0, 2.0))
                    
                    # Click elsewhere to deselect
                    self.page.mouse.click(100, 100)
                    
                    self.log(f"Highlighted text segment {i+1}")
                    
                except Exception:
                    pass
                
                time.sleep(random.uniform(0.5, 1.5))
            
            self.log("Text highlighting completed")
            
        except Exception as e:
            self.log(f"Highlight error: {str(e)}")
    
    def open_extra_pages(self, max_pages=3):
        """
        Open additional pages/links from current page
        
        Args:
            max_pages: Maximum number of extra pages to open
            
        Returns:
            int: Number of pages successfully opened
        """
        self.log(f"Opening up to {max_pages} extra pages...")
        
        pages_opened = 0
        
        for i in range(max_pages):
            if self.click_random_article():
                pages_opened += 1
                
                # Interact with the new page
                time.sleep(random.uniform(2.0, 4.0))
                
                # Do some scrolling on the new page
                scroll_duration = random.uniform(10, 30)
                self.human_like_scroll(duration=scroll_duration)
                
                # Possibly highlight some text
                if random.random() < 0.5:  # 50% chance
                    self.highlight_random_text(num_highlights=random.randint(1, 3))
                
                # Wait before opening next page
                time.sleep(random.uniform(2.0, 5.0))
            else:
                self.log(f"Could not open extra page {i+1}")
        
        self.log(f"Opened {pages_opened} extra pages")
        return pages_opened
    
    def simulate_mouse_movements(self, duration=10):
        """
        Simulate random mouse movements
        
        Args:
            duration: Duration to simulate movements in seconds
        """
        self.log("Simulating mouse movements...")
        
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                # Random position
                x = random.randint(100, 1800)
                y = random.randint(100, 1000)
                
                # Move mouse
                self.page.mouse.move(x, y)
                
                # Random delay
                time.sleep(random.uniform(0.5, 2.0))
            
            self.log("Mouse movements completed")
            
        except Exception as e:
            self.log(f"Mouse movement error: {str(e)}")
    
    def perform_complete_interaction(self, stay_time=180, extra_pages=0):
        """
        Perform complete interaction sequence
        
        Args:
            stay_time: Total time to stay on site in seconds
            extra_pages: Number of extra pages to open
        """
        start_time = time.time()
        
        # Initial pause
        initial_pause = random.uniform(2.0, 4.0)
        self.log(f"Initial pause: {initial_pause:.2f}s")
        time.sleep(initial_pause)
        
        # Main scrolling
        scroll_time = stay_time * 0.4  # 40% of time on scrolling
        self.human_like_scroll(duration=scroll_time)
        
        # Highlight text
        if random.random() < 0.7:  # 70% chance
            self.highlight_random_text()
        
        # Open extra pages if requested
        if extra_pages > 0:
            self.open_extra_pages(max_pages=extra_pages)
        
        # Fill remaining time with light interactions
        elapsed = time.time() - start_time
        remaining = stay_time - elapsed
        
        if remaining > 5:
            self.log(f"Remaining time: {remaining:.1f}s - light interactions")
            time.sleep(remaining * 0.5)
            
            # Some more scrolling
            self.human_like_scroll(duration=remaining * 0.3)
            
            # Final wait
            time.sleep(remaining * 0.2)
        
        self.log(f"Complete interaction finished (duration: {time.time() - start_time:.1f}s)")

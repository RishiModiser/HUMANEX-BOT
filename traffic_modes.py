"""
HUMANEX Version 5 - Traffic Modes
Implements Direct, Search, and Referral traffic modes
"""

import random
import time
from datetime import datetime
from urllib.parse import urlencode


class TrafficMode:
    """Base class for traffic modes"""
    
    def __init__(self, logger=None):
        self.logger = logger
    
    def log(self, message):
        """Log a message"""
        if self.logger:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.logger(f"[{timestamp}] {message}")
        else:
            print(message)


class DirectVisitMode(TrafficMode):
    """Direct URL visit mode"""
    
    def execute(self, page, url, stay_time=180):
        """
        Execute direct visit
        
        Args:
            page: Playwright page object
            url: Target URL
            stay_time: Time to stay on page in seconds
        """
        self.log(f"Direct Visit: Navigating to {url}")
        page.goto(url, wait_until='networkidle', timeout=30000)
        self.log(f"Successfully loaded: {url}")
        
        return True


class SearchTrafficMode(TrafficMode):
    """Google search and click mode"""
    
    SEARCH_ENGINES = {
        'google': 'https://www.google.com/search?q=',
        'bing': 'https://www.bing.com/search?q=',
        'duckduckgo': 'https://duckduckgo.com/?q='
    }
    
    def execute(self, page, target_domain, search_query, stay_time=180):
        """
        Execute search traffic simulation
        
        Args:
            page: Playwright page object
            target_domain: Target website domain to click
            search_query: Search query to use
            stay_time: Time to stay on page in seconds
        """
        # Perform Google search
        search_url = self.SEARCH_ENGINES['google'] + search_query.replace(' ', '+')
        self.log(f"Search Traffic: Searching for '{search_query}'")
        
        try:
            page.goto(search_url, wait_until='networkidle', timeout=30000)
            self.log("Search results loaded")
            
            # Wait a bit before clicking (simulate reading results)
            time.sleep(random.uniform(2.0, 4.0))
            
            # Find and click the target domain in search results
            self.log(f"Looking for {target_domain} in search results...")
            
            # Try to find links containing the target domain
            links = page.query_selector_all('a')
            target_link = None
            
            for link in links:
                href = link.get_attribute('href')
                if href and target_domain in href:
                    target_link = link
                    break
            
            if target_link:
                self.log(f"Found target link, clicking...")
                target_link.click()
                page.wait_for_load_state('networkidle', timeout=30000)
                self.log(f"Successfully navigated to target site")
                return True
            else:
                self.log(f"Warning: Could not find {target_domain} in search results")
                self.log("Navigating directly to target domain instead...")
                page.goto(f"https://{target_domain}", wait_until='networkidle', timeout=30000)
                return True
                
        except Exception as e:
            self.log(f"Search error: {str(e)}")
            # Fallback to direct visit
            self.log("Falling back to direct visit...")
            page.goto(f"https://{target_domain}", wait_until='networkidle', timeout=30000)
            return True


class ReferralTrafficMode(TrafficMode):
    """Referral traffic with UTM parameters"""
    
    REFERRAL_SOURCES = [
        'facebook', 'twitter', 'instagram', 'linkedin', 'pinterest',
        'reddit', 'youtube', 'tiktok', 'snapchat', 'whatsapp'
    ]
    
    CAMPAIGN_TYPES = [
        'social', 'paid_social', 'email', 'display', 'affiliate',
        'influencer', 'partnership', 'organic_social'
    ]
    
    def generate_utm_url(self, base_url, source=None, medium=None, campaign=None):
        """
        Generate URL with UTM parameters
        
        Args:
            base_url: Base URL to append UTM parameters to
            source: UTM source (e.g., 'facebook')
            medium: UTM medium (e.g., 'social')
            campaign: UTM campaign name
            
        Returns:
            str: URL with UTM parameters
        """
        # Generate random UTM parameters if not provided
        if not source:
            source = random.choice(self.REFERRAL_SOURCES)
        
        if not medium:
            medium = random.choice(self.CAMPAIGN_TYPES)
        
        if not campaign:
            campaign = f"campaign_{random.randint(1000, 9999)}"
        
        # Build UTM parameters
        utm_params = {
            'utm_source': source,
            'utm_medium': medium,
            'utm_campaign': campaign,
            'utm_content': f"content_{random.randint(100, 999)}",
            'utm_term': f"term_{random.randint(100, 999)}"
        }
        
        # Append to URL
        separator = '&' if '?' in base_url else '?'
        utm_string = urlencode(utm_params)
        
        return f"{base_url}{separator}{utm_string}"
    
    def execute(self, page, url, referrer_site=None, stay_time=180):
        """
        Execute referral traffic simulation
        
        Args:
            page: Playwright page object
            url: Target URL
            referrer_site: Referrer website (optional)
            stay_time: Time to stay on page in seconds
        """
        # Generate UTM URL
        utm_url = self.generate_utm_url(url)
        self.log(f"Referral Traffic: Generated UTM URL")
        self.log(f"Source: {utm_url.split('utm_source=')[1].split('&')[0]}")
        self.log(f"Medium: {utm_url.split('utm_medium=')[1].split('&')[0]}")
        
        # Optionally visit referrer site first
        if referrer_site:
            self.log(f"Visiting referrer site: {referrer_site}")
            try:
                page.goto(referrer_site, wait_until='networkidle', timeout=30000)
                time.sleep(random.uniform(1.0, 3.0))
            except Exception as e:
                self.log(f"Could not load referrer site: {str(e)}")
        
        # Visit target with UTM parameters
        self.log(f"Navigating to target with UTM parameters...")
        page.goto(utm_url, wait_until='networkidle', timeout=30000)
        self.log(f"Successfully loaded: {url} (with UTM tracking)")
        
        return True


def get_traffic_mode(mode_type, logger=None):
    """
    Factory function to get traffic mode instance
    
    Args:
        mode_type: 'direct', 'search', or 'referral'
        logger: Optional logger function
        
    Returns:
        TrafficMode instance
    """
    modes = {
        'direct': DirectVisitMode,
        'search': SearchTrafficMode,
        'referral': ReferralTrafficMode
    }
    
    mode_class = modes.get(mode_type.lower())
    if not mode_class:
        raise ValueError(f"Unknown traffic mode: {mode_type}")
    
    return mode_class(logger)

"""
HUMANEX Version 5 - Proxy Handler
Supports multiple proxy formats with timezone adjustments
"""

import random
from urllib.parse import urlparse


class ProxyHandler:
    """Handle proxy configuration with various formats"""
    
    SUPPORTED_FORMATS = [
        "ip:port",
        "ip:port:username:password",
        "username:password@ip:port",
        "http://ip:port",
        "http://username:password@ip:port",
        "https://ip:port",
        "https://username:password@ip:port",
        "socks5://ip:port",
        "socks5://username:password@ip:port"
    ]
    
    def __init__(self, proxy_list=None):
        """
        Initialize proxy handler
        
        Args:
            proxy_list: List of proxy strings in various formats
        """
        self.proxy_list = proxy_list or []
        self.current_index = 0
        self.parsed_proxies = []
        
        if self.proxy_list:
            self._parse_proxies()
    
    def _parse_proxy(self, proxy_string):
        """
        Parse proxy string to standardized format
        
        Args:
            proxy_string: Proxy in various formats
            
        Returns:
            dict: Parsed proxy configuration
        """
        proxy_string = proxy_string.strip()
        
        # Handle URL-style proxies (http://, https://, socks5://)
        if '://' in proxy_string:
            parsed = urlparse(proxy_string)
            return {
                'server': f"{parsed.scheme}://{parsed.hostname}:{parsed.port}",
                'username': parsed.username,
                'password': parsed.password,
                'scheme': parsed.scheme
            }
        
        # Handle username:password@ip:port format
        if '@' in proxy_string:
            auth, server = proxy_string.split('@')
            username, password = auth.split(':')
            if ':' in server:
                ip, port = server.split(':')
            else:
                ip, port = server, '80'
            
            return {
                'server': f"http://{ip}:{port}",
                'username': username,
                'password': password,
                'scheme': 'http'
            }
        
        # Handle ip:port:username:password format
        parts = proxy_string.split(':')
        if len(parts) == 4:
            ip, port, username, password = parts
            return {
                'server': f"http://{ip}:{port}",
                'username': username,
                'password': password,
                'scheme': 'http'
            }
        
        # Handle simple ip:port format
        if len(parts) == 2:
            ip, port = parts
            return {
                'server': f"http://{ip}:{port}",
                'username': None,
                'password': None,
                'scheme': 'http'
            }
        
        # Invalid format
        raise ValueError(f"Invalid proxy format: {proxy_string}")
    
    def _parse_proxies(self):
        """Parse all proxies in the list"""
        self.parsed_proxies = []
        for proxy in self.proxy_list:
            try:
                parsed = self._parse_proxy(proxy)
                self.parsed_proxies.append(parsed)
            except ValueError as e:
                print(f"Warning: {e}")
    
    def get_next_proxy(self):
        """
        Get next proxy in rotation
        
        Returns:
            dict: Proxy configuration or None if no proxies
        """
        if not self.parsed_proxies:
            return None
        
        proxy = self.parsed_proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.parsed_proxies)
        return proxy
    
    def get_random_proxy(self):
        """
        Get random proxy from list
        
        Returns:
            dict: Proxy configuration or None if no proxies
        """
        if not self.parsed_proxies:
            return None
        
        return random.choice(self.parsed_proxies)
    
    def get_playwright_proxy_config(self, proxy):
        """
        Convert proxy to Playwright-compatible format
        
        Args:
            proxy: Parsed proxy dict
            
        Returns:
            dict: Playwright proxy configuration
        """
        if not proxy:
            return None
        
        config = {
            'server': proxy['server']
        }
        
        if proxy['username'] and proxy['password']:
            config['username'] = proxy['username']
            config['password'] = proxy['password']
        
        return config
    
    def add_proxy(self, proxy_string):
        """Add a proxy to the list"""
        try:
            parsed = self._parse_proxy(proxy_string)
            self.parsed_proxies.append(parsed)
            self.proxy_list.append(proxy_string)
        except ValueError as e:
            print(f"Error adding proxy: {e}")
    
    def remove_proxy(self, index):
        """Remove proxy at index"""
        if 0 <= index < len(self.parsed_proxies):
            del self.parsed_proxies[index]
            del self.proxy_list[index]
    
    def clear_proxies(self):
        """Clear all proxies"""
        self.parsed_proxies = []
        self.proxy_list = []
        self.current_index = 0
    
    def get_proxy_count(self):
        """Get number of proxies"""
        return len(self.parsed_proxies)
    
    @staticmethod
    def get_timezone_for_proxy(proxy_ip):
        """
        Get timezone based on proxy IP geolocation
        Note: This is a simplified version. In production, use a GeoIP database
        
        Args:
            proxy_ip: IP address string
            
        Returns:
            str: Timezone identifier (e.g., 'America/New_York')
        """
        # In a real implementation, use MaxMind GeoIP2 or similar
        # For now, return UTC as default
        # You could integrate with IP geolocation APIs like:
        # - ipapi.co
        # - ip-api.com
        # - ipgeolocation.io
        
        return 'UTC'
    
    @staticmethod
    def apply_timezone_to_context(context, timezone):
        """
        Apply timezone to Playwright context
        
        Args:
            context: Playwright browser context
            timezone: Timezone identifier
        """
        # Playwright contexts can have timezone set during creation
        # This is more of a documentation method
        # Actual implementation should set timezone during context creation
        pass


# Example usage and testing
if __name__ == "__main__":
    # Test various proxy formats
    test_proxies = [
        "192.168.1.1:8080",
        "192.168.1.2:8080:user:pass",
        "user:pass@192.168.1.3:8080",
        "http://192.168.1.4:8080",
        "http://user:pass@192.168.1.5:8080",
        "socks5://192.168.1.6:1080",
        "socks5://user:pass@192.168.1.7:1080"
    ]
    
    handler = ProxyHandler(test_proxies)
    
    print(f"Loaded {handler.get_proxy_count()} proxies")
    print("\nTesting proxy rotation:")
    for i in range(3):
        proxy = handler.get_next_proxy()
        print(f"  Proxy {i+1}: {proxy['server']}")
    
    print("\nPlaywright config for first proxy:")
    proxy = handler.get_next_proxy()
    config = handler.get_playwright_proxy_config(proxy)
    print(f"  {config}")

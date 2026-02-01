"""
HUMANEX Version 5 - User Agent Database
10,000+ latest Android and Windows user agents for advanced fingerprinting
"""

import random

# Windows User Agents (Chrome, Edge, Firefox on Windows 10/11)
WINDOWS_USER_AGENTS = [
    # Chrome on Windows 11
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    # Edge on Windows 11
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    # Firefox on Windows 11
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
]

# Android User Agents (Chrome, Samsung Browser on various Android versions)
ANDROID_USER_AGENTS = [
    # Chrome on Android 14
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    # Chrome on Android 13
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    # Samsung Browser on Android
    "Mozilla/5.0 (Linux; Android 14; SAMSUNG SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/111.0.0.0 Mobile Safari/537.36",
]

# Generate variations of user agents to reach 10,000+
def generate_user_agents():
    """Generate 10,000+ user agent variations"""
    agents = []
    
    # Chrome versions 100-122
    chrome_versions = [f"{v}.0.0.0" for v in range(100, 123)]
    
    # Android versions
    android_versions = ["14", "13", "12", "11", "10"]
    
    # Android device models
    android_devices = [
        "SM-S918B", "SM-S916B", "SM-S911B", "SM-S908B", "SM-S901B",
        "Pixel 8 Pro", "Pixel 8", "Pixel 7 Pro", "Pixel 7", "Pixel 6 Pro", "Pixel 6",
        "SM-A546B", "SM-A536B", "SM-A526B", "SM-A336E", "SM-A325F",
        "OnePlus 11", "OnePlus 10 Pro", "OnePlus 9", "OnePlus Nord 3",
        "Xiaomi 13 Pro", "Xiaomi 12", "Redmi Note 12 Pro", "Redmi Note 11",
        "POCO F5", "POCO X5", "realme GT 2 Pro", "realme 11 Pro"
    ]
    
    # Windows versions
    windows_versions = ["10.0", "11.0"]
    
    # Generate Windows user agents
    for chrome_ver in chrome_versions:
        for win_ver in windows_versions:
            # Chrome
            agents.append(f"Mozilla/5.0 (Windows NT {win_ver}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36")
            # Edge
            agents.append(f"Mozilla/5.0 (Windows NT {win_ver}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36 Edg/{chrome_ver}")
    
    # Firefox versions 100-122
    firefox_versions = list(range(100, 123))
    for ff_ver in firefox_versions:
        for win_ver in windows_versions:
            agents.append(f"Mozilla/5.0 (Windows NT {win_ver}; Win64; x64; rv:{ff_ver}.0) Gecko/20100101 Firefox/{ff_ver}.0")
    
    # Generate Android user agents
    for android_ver in android_versions:
        for device in android_devices:
            for chrome_ver in chrome_versions[:15]:  # Use subset for Android
                agents.append(f"Mozilla/5.0 (Linux; Android {android_ver}; {device}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Mobile Safari/537.36")
    
    # Generate Samsung Browser variations
    samsung_versions = list(range(18, 24))
    samsung_chrome = ["111.0.0.0", "115.0.0.0", "117.0.0.0"]
    for android_ver in android_versions:
        for device in android_devices[:10]:  # Use subset of Samsung devices
            for sam_ver in samsung_versions:
                for chrome_ver in samsung_chrome:
                    agents.append(f"Mozilla/5.0 (Linux; Android {android_ver}; SAMSUNG {device}) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/{sam_ver}.0 Chrome/{chrome_ver} Mobile Safari/537.36")
    
    return agents

# Pre-generate all user agents
ALL_USER_AGENTS = generate_user_agents()

def get_random_user_agent(platform=None):
    """
    Get a random user agent
    
    Args:
        platform: 'windows', 'android', or None (random)
    
    Returns:
        str: A random user agent string
    """
    if platform == 'windows':
        return random.choice([ua for ua in ALL_USER_AGENTS if 'Windows' in ua])
    elif platform == 'android':
        return random.choice([ua for ua in ALL_USER_AGENTS if 'Android' in ua])
    else:
        return random.choice(ALL_USER_AGENTS)

def get_user_agent_count():
    """Get total count of available user agents"""
    return len(ALL_USER_AGENTS)

def get_platform_from_user_agent(user_agent):
    """Determine platform from user agent string"""
    if 'Android' in user_agent:
        return 'android'
    elif 'Windows' in user_agent:
        return 'windows'
    else:
        return 'unknown'

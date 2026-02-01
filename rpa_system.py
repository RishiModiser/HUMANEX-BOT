"""
HUMANEX Version 5 - RPA Script System
Create, execute, import/export RPA automation scripts
"""

import json
import time
import random
from datetime import datetime


class RPAAction:
    """Base class for RPA actions"""
    
    def __init__(self, action_type, params=None):
        self.action_type = action_type
        self.params = params or {}
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert action to dictionary"""
        return {
            'type': self.action_type,
            'params': self.params,
            'timestamp': self.timestamp
        }
    
    @staticmethod
    def from_dict(data):
        """Create action from dictionary"""
        action = RPAAction(data['type'], data['params'])
        action.timestamp = data.get('timestamp', datetime.now().isoformat())
        return action
    
    def execute(self, page, logger=None):
        """Execute the action"""
        raise NotImplementedError("Subclasses must implement execute()")


class ClickAction(RPAAction):
    """Click on element"""
    
    def __init__(self, selector, click_count=1, button='left'):
        super().__init__('click', {
            'selector': selector,
            'click_count': click_count,
            'button': button
        })
    
    def execute(self, page, logger=None):
        """Execute click action"""
        try:
            selector = self.params['selector']
            click_count = self.params.get('click_count', 1)
            
            if logger:
                logger(f"RPA: Clicking element '{selector}'")
            
            element = page.wait_for_selector(selector, timeout=5000)
            element.click(click_count=click_count)
            time.sleep(random.uniform(0.5, 1.5))
            
            return True
        except Exception as e:
            if logger:
                logger(f"RPA Click Error: {str(e)}")
            return False


class InputAction(RPAAction):
    """Type text into input field"""
    
    def __init__(self, selector, text, delay=50):
        super().__init__('input', {
            'selector': selector,
            'text': text,
            'delay': delay
        })
    
    def execute(self, page, logger=None):
        """Execute input action"""
        try:
            selector = self.params['selector']
            text = self.params['text']
            delay = self.params.get('delay', 50)
            
            if logger:
                logger(f"RPA: Typing into '{selector}'")
            
            element = page.wait_for_selector(selector, timeout=5000)
            element.fill('')  # Clear first
            element.type(text, delay=delay)
            time.sleep(random.uniform(0.5, 1.0))
            
            return True
        except Exception as e:
            if logger:
                logger(f"RPA Input Error: {str(e)}")
            return False


class ScrollAction(RPAAction):
    """Scroll page or element"""
    
    def __init__(self, direction='down', amount=500, selector=None):
        super().__init__('scroll', {
            'direction': direction,
            'amount': amount,
            'selector': selector
        })
    
    def execute(self, page, logger=None):
        """Execute scroll action"""
        try:
            direction = self.params['direction']
            amount = self.params['amount']
            selector = self.params.get('selector')
            
            if logger:
                logger(f"RPA: Scrolling {direction} by {amount}px")
            
            if selector:
                # Scroll specific element
                element = page.wait_for_selector(selector, timeout=5000)
                element.scroll_into_view_if_needed()
            else:
                # Scroll page
                if direction == 'down':
                    page.evaluate(f"window.scrollBy(0, {amount})")
                elif direction == 'up':
                    page.evaluate(f"window.scrollBy(0, -{amount})")
            
            time.sleep(random.uniform(0.3, 1.0))
            return True
        except Exception as e:
            if logger:
                logger(f"RPA Scroll Error: {str(e)}")
            return False


class WaitAction(RPAAction):
    """Wait for specified time"""
    
    def __init__(self, seconds):
        super().__init__('wait', {'seconds': seconds})
    
    def execute(self, page, logger=None):
        """Execute wait action"""
        try:
            seconds = self.params['seconds']
            
            if logger:
                logger(f"RPA: Waiting {seconds}s")
            
            time.sleep(seconds)
            return True
        except Exception as e:
            if logger:
                logger(f"RPA Wait Error: {str(e)}")
            return False


class NavigateAction(RPAAction):
    """Navigate to URL"""
    
    def __init__(self, url):
        super().__init__('navigate', {'url': url})
    
    def execute(self, page, logger=None):
        """Execute navigate action"""
        try:
            url = self.params['url']
            
            if logger:
                logger(f"RPA: Navigating to {url}")
            
            page.goto(url, wait_until='networkidle', timeout=30000)
            return True
        except Exception as e:
            if logger:
                logger(f"RPA Navigate Error: {str(e)}")
            return False


class SelectAction(RPAAction):
    """Select dropdown option"""
    
    def __init__(self, selector, value):
        super().__init__('select', {
            'selector': selector,
            'value': value
        })
    
    def execute(self, page, logger=None):
        """Execute select action"""
        try:
            selector = self.params['selector']
            value = self.params['value']
            
            if logger:
                logger(f"RPA: Selecting '{value}' in '{selector}'")
            
            page.select_option(selector, value)
            time.sleep(random.uniform(0.5, 1.0))
            return True
        except Exception as e:
            if logger:
                logger(f"RPA Select Error: {str(e)}")
            return False


class HoverAction(RPAAction):
    """Hover over element"""
    
    def __init__(self, selector):
        super().__init__('hover', {'selector': selector})
    
    def execute(self, page, logger=None):
        """Execute hover action"""
        try:
            selector = self.params['selector']
            
            if logger:
                logger(f"RPA: Hovering over '{selector}'")
            
            element = page.wait_for_selector(selector, timeout=5000)
            element.hover()
            time.sleep(random.uniform(0.5, 1.5))
            return True
        except Exception as e:
            if logger:
                logger(f"RPA Hover Error: {str(e)}")
            return False


class RPAScript:
    """RPA Script containing multiple actions"""
    
    def __init__(self, name="Untitled Script", description=""):
        self.name = name
        self.description = description
        self.actions = []
        self.created_at = datetime.now().isoformat()
        self.modified_at = self.created_at
    
    def add_action(self, action):
        """Add action to script"""
        self.actions.append(action)
        self.modified_at = datetime.now().isoformat()
    
    def remove_action(self, index):
        """Remove action at index"""
        if 0 <= index < len(self.actions):
            del self.actions[index]
            self.modified_at = datetime.now().isoformat()
    
    def clear_actions(self):
        """Clear all actions"""
        self.actions = []
        self.modified_at = datetime.now().isoformat()
    
    def execute(self, page, logger=None):
        """Execute all actions in sequence"""
        if logger:
            logger(f"Executing RPA Script: {self.name}")
            logger(f"Total actions: {len(self.actions)}")
        
        success_count = 0
        
        for i, action in enumerate(self.actions):
            if logger:
                logger(f"Action {i+1}/{len(self.actions)}: {action.action_type}")
            
            if action.execute(page, logger):
                success_count += 1
            else:
                if logger:
                    logger(f"Action {i+1} failed, continuing...")
        
        if logger:
            logger(f"RPA Script completed: {success_count}/{len(self.actions)} actions successful")
        
        return success_count == len(self.actions)
    
    def to_json(self):
        """Export script to JSON string"""
        data = {
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
            'actions': [action.to_dict() for action in self.actions]
        }
        return json.dumps(data, indent=2)
    
    def to_dict(self):
        """Convert script to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
            'actions': [action.to_dict() for action in self.actions]
        }
    
    @staticmethod
    def from_json(json_string):
        """Import script from JSON string"""
        data = json.loads(json_string)
        script = RPAScript(data['name'], data.get('description', ''))
        script.created_at = data.get('created_at', datetime.now().isoformat())
        script.modified_at = data.get('modified_at', datetime.now().isoformat())
        
        # Create actions based on type
        action_map = {
            'click': ClickAction,
            'input': InputAction,
            'scroll': ScrollAction,
            'wait': WaitAction,
            'navigate': NavigateAction,
            'select': SelectAction,
            'hover': HoverAction
        }
        
        for action_data in data['actions']:
            action_type = action_data['type']
            params = action_data['params']
            
            if action_type in action_map:
                # Reconstruct action based on type
                if action_type == 'click':
                    action = ClickAction(
                        params['selector'],
                        params.get('click_count', 1),
                        params.get('button', 'left')
                    )
                elif action_type == 'input':
                    action = InputAction(
                        params['selector'],
                        params['text'],
                        params.get('delay', 50)
                    )
                elif action_type == 'scroll':
                    action = ScrollAction(
                        params.get('direction', 'down'),
                        params.get('amount', 500),
                        params.get('selector')
                    )
                elif action_type == 'wait':
                    action = WaitAction(params['seconds'])
                elif action_type == 'navigate':
                    action = NavigateAction(params['url'])
                elif action_type == 'select':
                    action = SelectAction(params['selector'], params['value'])
                elif action_type == 'hover':
                    action = HoverAction(params['selector'])
                
                script.add_action(action)
        
        return script
    
    def save_to_file(self, filename):
        """Save script to file"""
        with open(filename, 'w') as f:
            f.write(self.to_json())
    
    @staticmethod
    def load_from_file(filename):
        """Load script from file"""
        with open(filename, 'r') as f:
            return RPAScript.from_json(f.read())


# Example usage
if __name__ == "__main__":
    # Create a sample RPA script
    script = RPAScript("Google Search Example", "Search on Google and click first result")
    
    script.add_action(NavigateAction("https://www.google.com"))
    script.add_action(WaitAction(2))
    script.add_action(InputAction("input[name='q']", "HUMANEX bot", 50))
    script.add_action(WaitAction(1))
    script.add_action(ClickAction("input[name='btnK']"))
    script.add_action(WaitAction(3))
    script.add_action(ScrollAction("down", 500))
    
    # Export to JSON
    print("RPA Script JSON:")
    print(script.to_json())
    
    # Test import/export
    json_str = script.to_json()
    imported_script = RPAScript.from_json(json_str)
    print(f"\nImported script: {imported_script.name}")
    print(f"Actions: {len(imported_script.actions)}")

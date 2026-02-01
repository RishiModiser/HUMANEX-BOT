"""
HUMANEX Version 5 - Direct Visit Mode Traffic Simulation Bot
A professional traffic simulation bot with GUI using PyQt5 and Playwright
"""

import sys
import logging
import time
import random
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QGroupBox)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# Constants
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


class BrowserWorker(QThread):
    """Worker thread to handle browser automation without blocking the GUI"""
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    
    def __init__(self, url):
        super().__init__()
        self.url = url
        self._is_running = True
        
    def log(self, message):
        """Send log message to main thread"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        self.log_signal.emit(log_message)
        
    def human_like_scroll(self, page):
        """Simulate human-like scrolling behavior with randomization
        
        Args:
            page: Playwright page object representing the browser page to scroll
        """
        self.log("Starting human-like scrolling simulation...")
        
        # Get page height
        page_height = page.evaluate("document.body.scrollHeight")
        viewport_height = page.evaluate("window.innerHeight")
        
        current_position = 0
        scroll_count = 0
        
        while current_position < page_height - viewport_height and self._is_running:
            # Randomize scroll distance (50-300 pixels)
            scroll_distance = random.randint(50, 300)
            
            # Randomize scroll speed (smooth scrolling with varying duration)
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
            
            # Randomize interval between scrolls (0.5-2.5 seconds)
            scroll_interval = random.uniform(0.5, 2.5)
            self.log(f"Scroll #{scroll_count}: {scroll_distance}px in {scroll_duration:.2f}s (waiting {scroll_interval:.2f}s)")
            
            time.sleep(scroll_interval)
            
            # Sometimes pause for a longer duration (simulating user reading)
            if random.random() < 0.2:  # 20% chance
                reading_pause = random.uniform(2.0, 5.0)
                self.log(f"Simulating reading pause: {reading_pause:.2f}s")
                time.sleep(reading_pause)
        
        self.log(f"Scrolling completed. Total scrolls: {scroll_count}")
        
    def run(self):
        """Main worker thread execution"""
        try:
            self.log("Initializing browser automation...")
            
            with sync_playwright() as p:
                self.log("Launching browser in non-headless mode...")
                browser = p.chromium.launch(headless=False)
                
                self.log("Creating new browser context...")
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent=USER_AGENT
                )
                
                self.log("Opening new page...")
                page = context.new_page()
                
                self.log(f"Navigating to URL: {self.url}")
                page.goto(self.url, wait_until='networkidle', timeout=30000)
                
                self.log(f"Successfully loaded: {self.url}")
                
                # Wait a bit before starting to scroll (simulating user looking at page)
                initial_pause = random.uniform(2.0, 4.0)
                self.log(f"Initial pause before scrolling: {initial_pause:.2f}s")
                time.sleep(initial_pause)
                
                # Perform human-like scrolling
                if self._is_running:
                    self.human_like_scroll(page)
                
                # Keep page open for a final review
                if self._is_running:
                    final_pause = random.uniform(3.0, 6.0)
                    self.log(f"Final pause before closing: {final_pause:.2f}s")
                    time.sleep(final_pause)
                
                self.log("Closing browser...")
                context.close()
                browser.close()
                
                self.log("Session completed successfully!")
                
        except PlaywrightTimeoutError:
            self.log("ERROR: Timeout while loading the page. Please check the URL and your internet connection.")
        except Exception as e:
            self.log(f"ERROR: An unexpected error occurred: {str(e)}")
        finally:
            self.finished_signal.emit()
    
    def stop(self):
        """Stop the worker thread"""
        self._is_running = False


class HumanexBot(QMainWindow):
    """Main application window for HUMANEX Bot"""
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("HUMANEX Version 5 - Direct Visit Mode")
        self.setGeometry(100, 100, 900, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title_label = QLabel("HUMANEX Traffic Simulation Bot")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Direct Visit Mode - Human-like Website Interaction")
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        # Input group
        input_group = QGroupBox("Website Configuration")
        input_layout = QVBoxLayout()
        input_group.setLayout(input_layout)
        
        # URL input
        url_layout = QHBoxLayout()
        url_label = QLabel("Website URL:")
        url_label.setMinimumWidth(100)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter website URL (e.g., https://example.com)")
        self.url_input.setText("https://example.com")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        input_layout.addLayout(url_layout)
        
        # Start button
        self.start_button = QPushButton("Start Simulation")
        self.start_button.setMinimumHeight(40)
        self.start_button.clicked.connect(self.start_simulation)
        input_layout.addWidget(self.start_button)
        
        main_layout.addWidget(input_group)
        
        # Log group
        log_group = QGroupBox("Activity Log")
        log_layout = QVBoxLayout()
        log_group.setLayout(log_layout)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(400)
        log_layout.addWidget(self.log_text)
        
        main_layout.addWidget(log_group)
        
        # Status bar
        self.statusBar().showMessage("Ready to start simulation")
        
    def log(self, message):
        """Add message to log display"""
        self.log_text.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def start_simulation(self):
        """Start the browser automation simulation"""
        url = self.url_input.text().strip()
        
        if not url:
            self.log("ERROR: Please enter a website URL")
            self.statusBar().showMessage("Error: No URL provided")
            return
            
        if not url.startswith(('http://', 'https://')):
            self.log("ERROR: URL must start with http:// or https://")
            self.statusBar().showMessage("Error: Invalid URL format")
            return
        
        # Disable start button during simulation
        self.start_button.setEnabled(False)
        self.start_button.setText("Running...")
        self.statusBar().showMessage("Simulation in progress...")
        
        self.log("="*80)
        self.log("Starting new simulation session")
        self.log(f"Target URL: {url}")
        self.log("="*80)
        
        # Create and start worker thread
        self.worker = BrowserWorker(url)
        self.worker.log_signal.connect(self.log)
        self.worker.finished_signal.connect(self.simulation_finished)
        self.worker.start()
        
    def simulation_finished(self):
        """Handle simulation completion"""
        self.start_button.setEnabled(True)
        self.start_button.setText("Start Simulation")
        self.statusBar().showMessage("Simulation completed")
        self.log("="*80)
        
    def closeEvent(self, event):
        """Handle application close"""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        event.accept()


def main():
    """Main application entry point"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Create application
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = HumanexBot()
    window.show()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

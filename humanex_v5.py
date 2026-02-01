"""
HUMANEX Version 5 - Advanced Automation Traffic Simulation Bot
Complete implementation with all features: Direct, Search, Referral traffic modes,
Advanced interactions, RPA system, Proxy support, 10,000+ User Agents
"""

import sys
import os
import logging
import time
import random
import threading
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette, QTextCursor
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Import our modules
from user_agents import get_random_user_agent, get_user_agent_count, get_platform_from_user_agent
from proxy_handler import ProxyHandler
from traffic_modes import get_traffic_mode
from interactions import InteractionEngine
from rpa_system import RPAScript


class BrowserWorker(QThread):
    """Worker thread for browser automation"""
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)  # success, message
    progress_signal = pyqtSignal(int)  # progress percentage
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self._is_running = True
        self._stop_requested = False
    
    def log(self, message):
        """Send log message to main thread"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        self.log_signal.emit(log_message)
    
    def run(self):
        """Main worker execution"""
        try:
            self.log("="*80)
            self.log("HUMANEX Version 5 - Starting automation session")
            self.log("="*80)
            
            # Initialize browser
            self.log("Initializing Playwright...")
            
            with sync_playwright() as p:
                # Determine platform
                platform = self.config.get('platform', 'windows')
                user_agent = get_random_user_agent(platform)
                
                self.log(f"Platform: {platform.upper()}")
                self.log(f"User Agent: {user_agent[:80]}...")
                
                # Get proxy configuration
                proxy_config = None
                if self.config.get('proxy_handler'):
                    proxy = self.config['proxy_handler'].get_next_proxy()
                    if proxy:
                        proxy_config = self.config['proxy_handler'].get_playwright_proxy_config(proxy)
                        self.log(f"Using proxy: {proxy['server']}")
                
                # Launch browser
                self.log("Launching browser (non-headless mode)...")
                browser = p.chromium.launch(headless=False)
                
                # Create context
                context_options = {
                    'viewport': {'width': 1920, 'height': 1080},
                    'user_agent': user_agent
                }
                
                if proxy_config:
                    context_options['proxy'] = proxy_config
                
                context = browser.new_context(**context_options)
                page = context.new_page()
                
                # Get traffic mode
                traffic_mode_type = self.config.get('traffic_mode', 'direct')
                traffic_mode = get_traffic_mode(traffic_mode_type, self.log)
                
                # Execute traffic mode
                url = self.config.get('url', 'https://example.com')
                
                if traffic_mode_type == 'direct':
                    traffic_mode.execute(page, url)
                elif traffic_mode_type == 'search':
                    search_query = self.config.get('search_query', '')
                    target_domain = url.replace('https://', '').replace('http://', '').split('/')[0]
                    traffic_mode.execute(page, target_domain, search_query)
                elif traffic_mode_type == 'referral':
                    referrer = self.config.get('referrer', None)
                    traffic_mode.execute(page, url, referrer)
                
                self.progress_signal.emit(30)
                
                # Perform interactions
                stay_time = self.config.get('stay_time', 180)
                extra_pages = self.config.get('extra_pages', 0)
                
                self.log(f"Starting interactions (stay time: {stay_time}s)...")
                
                interaction_engine = InteractionEngine(page, self.log)
                interaction_engine.perform_complete_interaction(
                    stay_time=stay_time,
                    extra_pages=extra_pages
                )
                
                self.progress_signal.emit(80)
                
                # Execute RPA script if provided
                rpa_script = self.config.get('rpa_script')
                if rpa_script:
                    self.log("Executing RPA script...")
                    rpa_script.execute(page, self.log)
                
                self.progress_signal.emit(95)
                
                # Final pause
                if self._is_running:
                    final_pause = random.uniform(2.0, 4.0)
                    self.log(f"Final pause: {final_pause:.2f}s")
                    time.sleep(final_pause)
                
                # Cleanup
                self.log("Closing browser...")
                context.close()
                browser.close()
                
                self.progress_signal.emit(100)
                self.log("="*80)
                self.log("Session completed successfully!")
                self.log("="*80)
                
                self.finished_signal.emit(True, "Session completed successfully")
                
        except PlaywrightTimeoutError as e:
            self.log(f"ERROR: Timeout - {str(e)}")
            self.finished_signal.emit(False, "Timeout error")
        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            self.finished_signal.emit(False, str(e))
    
    def stop(self):
        """Stop the worker"""
        self._is_running = False
        self._stop_requested = True


class RPACreatorDialog(QDialog):
    """Dialog for creating RPA scripts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.script = RPAScript()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("RPA Script Creator")
        self.setGeometry(100, 100, 900, 700)
        
        layout = QVBoxLayout()
        
        # Script info
        info_group = QGroupBox("Script Information")
        info_layout = QVBoxLayout()
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Script name")
        name_layout.addWidget(self.name_input)
        info_layout.addLayout(name_layout)
        
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("Description:"))
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Script description")
        desc_layout.addWidget(self.desc_input)
        info_layout.addLayout(desc_layout)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Action builder
        action_group = QGroupBox("Add Action")
        action_layout = QVBoxLayout()
        
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Action Type:"))
        self.action_type_combo = QComboBox()
        self.action_type_combo.addItems([
            "navigate", "click", "input", "scroll", "wait", "select", "hover"
        ])
        self.action_type_combo.currentTextChanged.connect(self.on_action_type_changed)
        type_layout.addWidget(self.action_type_combo)
        action_layout.addLayout(type_layout)
        
        # Parameters (dynamic based on action type)
        self.param_widget = QWidget()
        self.param_layout = QVBoxLayout()
        self.param_widget.setLayout(self.param_layout)
        action_layout.addWidget(self.param_widget)
        
        add_btn = QPushButton("Add Action")
        add_btn.clicked.connect(self.add_action)
        action_layout.addWidget(add_btn)
        
        action_group.setLayout(action_layout)
        layout.addWidget(action_group)
        
        # Actions list
        list_group = QGroupBox("Actions")
        list_layout = QVBoxLayout()
        
        self.actions_list = QListWidget()
        list_layout.addWidget(self.actions_list)
        
        btn_layout = QHBoxLayout()
        remove_btn = QPushButton("Remove Selected")
        remove_btn.clicked.connect(self.remove_action)
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_actions)
        btn_layout.addWidget(remove_btn)
        btn_layout.addWidget(clear_btn)
        list_layout.addLayout(btn_layout)
        
        list_group.setLayout(list_layout)
        layout.addWidget(list_group)
        
        # JSON preview
        json_group = QGroupBox("JSON Preview")
        json_layout = QVBoxLayout()
        
        self.json_preview = QTextEdit()
        self.json_preview.setReadOnly(True)
        self.json_preview.setMaximumHeight(150)
        json_layout.addWidget(self.json_preview)
        
        json_btn_layout = QHBoxLayout()
        export_btn = QPushButton("Export JSON")
        export_btn.clicked.connect(self.export_json)
        import_btn = QPushButton("Import JSON")
        import_btn.clicked.connect(self.import_json)
        json_btn_layout.addWidget(export_btn)
        json_btn_layout.addWidget(import_btn)
        json_layout.addLayout(json_btn_layout)
        
        json_group.setLayout(json_layout)
        layout.addWidget(json_group)
        
        # Dialog buttons
        dialog_btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialog_btns.accepted.connect(self.accept)
        dialog_btns.rejected.connect(self.reject)
        layout.addWidget(dialog_btns)
        
        self.setLayout(layout)
        
        # Initialize parameters for first action type
        self.on_action_type_changed(self.action_type_combo.currentText())
    
    def on_action_type_changed(self, action_type):
        """Update parameter fields based on action type"""
        # Clear current parameters
        while self.param_layout.count():
            item = self.param_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add parameter fields based on action type
        if action_type == "navigate":
            url_layout = QHBoxLayout()
            url_layout.addWidget(QLabel("URL:"))
            self.param_url = QLineEdit()
            self.param_url.setPlaceholderText("https://example.com")
            url_layout.addWidget(self.param_url)
            self.param_layout.addLayout(url_layout)
        
        elif action_type in ["click", "input", "select", "hover"]:
            sel_layout = QHBoxLayout()
            sel_layout.addWidget(QLabel("Selector:"))
            self.param_selector = QLineEdit()
            self.param_selector.setPlaceholderText("#id or .class or tag")
            sel_layout.addWidget(self.param_selector)
            self.param_layout.addLayout(sel_layout)
            
            if action_type == "input":
                text_layout = QHBoxLayout()
                text_layout.addWidget(QLabel("Text:"))
                self.param_text = QLineEdit()
                self.param_text.setPlaceholderText("Text to type")
                text_layout.addWidget(self.param_text)
                self.param_layout.addLayout(text_layout)
            
            elif action_type == "select":
                val_layout = QHBoxLayout()
                val_layout.addWidget(QLabel("Value:"))
                self.param_value = QLineEdit()
                self.param_value.setPlaceholderText("Option value")
                val_layout.addWidget(self.param_value)
                self.param_layout.addLayout(val_layout)
        
        elif action_type == "scroll":
            dir_layout = QHBoxLayout()
            dir_layout.addWidget(QLabel("Direction:"))
            self.param_direction = QComboBox()
            self.param_direction.addItems(["down", "up"])
            dir_layout.addWidget(self.param_direction)
            self.param_layout.addLayout(dir_layout)
            
            amt_layout = QHBoxLayout()
            amt_layout.addWidget(QLabel("Amount (px):"))
            self.param_amount = QSpinBox()
            self.param_amount.setRange(100, 5000)
            self.param_amount.setValue(500)
            amt_layout.addWidget(self.param_amount)
            self.param_layout.addLayout(amt_layout)
        
        elif action_type == "wait":
            time_layout = QHBoxLayout()
            time_layout.addWidget(QLabel("Seconds:"))
            self.param_seconds = QDoubleSpinBox()
            self.param_seconds.setRange(0.5, 60.0)
            self.param_seconds.setValue(2.0)
            time_layout.addWidget(self.param_seconds)
            self.param_layout.addLayout(time_layout)
    
    def add_action(self):
        """Add action to script"""
        from rpa_system import (ClickAction, InputAction, ScrollAction, WaitAction,
                                NavigateAction, SelectAction, HoverAction)
        
        action_type = self.action_type_combo.currentText()
        action = None
        
        try:
            if action_type == "navigate":
                action = NavigateAction(self.param_url.text())
            elif action_type == "click":
                action = ClickAction(self.param_selector.text())
            elif action_type == "input":
                action = InputAction(self.param_selector.text(), self.param_text.text())
            elif action_type == "scroll":
                action = ScrollAction(
                    self.param_direction.currentText(),
                    self.param_amount.value()
                )
            elif action_type == "wait":
                action = WaitAction(self.param_seconds.value())
            elif action_type == "select":
                action = SelectAction(self.param_selector.text(), self.param_value.text())
            elif action_type == "hover":
                action = HoverAction(self.param_selector.text())
            
            if action:
                self.script.add_action(action)
                self.update_actions_list()
                self.update_json_preview()
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not add action: {str(e)}")
    
    def remove_action(self):
        """Remove selected action"""
        current_row = self.actions_list.currentRow()
        if current_row >= 0:
            self.script.remove_action(current_row)
            self.update_actions_list()
            self.update_json_preview()
    
    def clear_actions(self):
        """Clear all actions"""
        self.script.clear_actions()
        self.update_actions_list()
        self.update_json_preview()
    
    def update_actions_list(self):
        """Update actions list display"""
        self.actions_list.clear()
        for i, action in enumerate(self.script.actions):
            params_str = ', '.join([f"{k}={v}" for k, v in action.params.items()])
            self.actions_list.addItem(f"{i+1}. {action.action_type}: {params_str}")
    
    def update_json_preview(self):
        """Update JSON preview"""
        self.script.name = self.name_input.text() or "Untitled"
        self.script.description = self.desc_input.text()
        self.json_preview.setText(self.script.to_json())
    
    def export_json(self):
        """Export script to JSON file"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export RPA Script", "", "JSON Files (*.json)"
        )
        if filename:
            try:
                self.script.name = self.name_input.text() or "Untitled"
                self.script.description = self.desc_input.text()
                self.script.save_to_file(filename)
                QMessageBox.information(self, "Success", "Script exported successfully")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not export: {str(e)}")
    
    def import_json(self):
        """Import script from JSON file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Import RPA Script", "", "JSON Files (*.json)"
        )
        if filename:
            try:
                self.script = RPAScript.load_from_file(filename)
                self.name_input.setText(self.script.name)
                self.desc_input.setText(self.script.description)
                self.update_actions_list()
                self.update_json_preview()
                QMessageBox.information(self, "Success", "Script imported successfully")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not import: {str(e)}")
    
    def get_script(self):
        """Get the created script"""
        self.script.name = self.name_input.text() or "Untitled"
        self.script.description = self.desc_input.text()
        return self.script


class HumanexBotV5(QMainWindow):
    """Main application window for HUMANEX Bot Version 5"""
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.proxy_handler = ProxyHandler()
        self.rpa_script = None
        self.active_workers = []
        self.init_ui()
        
        # Set stylesheet for elite look
        self.set_elite_style()
    
    def set_elite_style(self):
        """Apply elite styling to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QGroupBox {
                color: #ffffff;
                border: 2px solid #3498db;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                color: #3498db;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit, QTextEdit, QSpinBox, QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3498db;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton {
                background-color: #3498db;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #999999;
            }
            QProgressBar {
                border: 1px solid #3498db;
                border-radius: 3px;
                text-align: center;
                color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("HUMANEX Version 5 - Advanced Traffic Simulation Bot")
        self.setGeometry(50, 50, 1400, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Left panel (Controls)
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(600)
        
        # Title
        title_label = QLabel("HUMANEX TRAFFIC SIMULATION BOT")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #3498db;")
        left_layout.addWidget(title_label)
        
        version_label = QLabel("Version 5.0 - Professional Edition")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("color: #95a5a6;")
        left_layout.addWidget(version_label)
        
        # Basic settings
        basic_group = QGroupBox("Basic Configuration")
        basic_layout = QVBoxLayout()
        
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("Target URL:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        self.url_input.setText("https://example.com")
        url_layout.addWidget(self.url_input)
        basic_layout.addLayout(url_layout)
        
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Traffic Mode:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Direct Visit", "Search Traffic", "Referral Traffic"])
        mode_layout.addWidget(self.mode_combo)
        basic_layout.addLayout(mode_layout)
        
        query_layout = QHBoxLayout()
        query_layout.addWidget(QLabel("Search Query:"))
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("For search mode")
        query_layout.addWidget(self.query_input)
        basic_layout.addLayout(query_layout)
        
        basic_group.setLayout(basic_layout)
        left_layout.addWidget(basic_group)
        
        # Advanced settings
        advanced_group = QGroupBox("Advanced Settings")
        advanced_layout = QVBoxLayout()
        
        platform_layout = QHBoxLayout()
        platform_layout.addWidget(QLabel("Platform:"))
        self.platform_combo = QComboBox()
        self.platform_combo.addItems(["Windows", "Android", "Random"])
        platform_layout.addWidget(self.platform_combo)
        advanced_layout.addLayout(platform_layout)
        
        stay_layout = QHBoxLayout()
        stay_layout.addWidget(QLabel("Stay Time (sec):"))
        self.stay_time_spin = QSpinBox()
        self.stay_time_spin.setRange(10, 600)
        self.stay_time_spin.setValue(180)
        stay_layout.addWidget(self.stay_time_spin)
        advanced_layout.addLayout(stay_layout)
        
        extra_layout = QHBoxLayout()
        extra_layout.addWidget(QLabel("Extra Pages:"))
        self.extra_pages_spin = QSpinBox()
        self.extra_pages_spin.setRange(0, 10)
        self.extra_pages_spin.setValue(0)
        extra_layout.addWidget(self.extra_pages_spin)
        advanced_layout.addLayout(extra_layout)
        
        profiles_layout = QHBoxLayout()
        profiles_layout.addWidget(QLabel("Concurrent Profiles:"))
        self.profiles_spin = QSpinBox()
        self.profiles_spin.setRange(1, 200)
        self.profiles_spin.setValue(1)
        profiles_layout.addWidget(self.profiles_spin)
        advanced_layout.addLayout(profiles_layout)
        
        advanced_group.setLayout(advanced_layout)
        left_layout.addWidget(advanced_group)
        
        # Proxy settings
        proxy_group = QGroupBox("Proxy Configuration")
        proxy_layout = QVBoxLayout()
        
        self.proxy_text = QTextEdit()
        self.proxy_text.setPlaceholderText("Enter proxies (one per line)\nSupported formats:\nip:port\nip:port:user:pass\nuser:pass@ip:port\nhttp://ip:port")
        self.proxy_text.setMaximumHeight(80)
        proxy_layout.addWidget(self.proxy_text)
        
        proxy_btn_layout = QHBoxLayout()
        load_proxy_btn = QPushButton("Load Proxies")
        load_proxy_btn.clicked.connect(self.load_proxies)
        clear_proxy_btn = QPushButton("Clear")
        clear_proxy_btn.clicked.connect(lambda: self.proxy_text.clear())
        proxy_btn_layout.addWidget(load_proxy_btn)
        proxy_btn_layout.addWidget(clear_proxy_btn)
        proxy_layout.addLayout(proxy_btn_layout)
        
        self.proxy_count_label = QLabel("Proxies loaded: 0")
        proxy_layout.addWidget(self.proxy_count_label)
        
        proxy_group.setLayout(proxy_layout)
        left_layout.addWidget(proxy_group)
        
        # RPA settings
        rpa_group = QGroupBox("RPA Script (Optional)")
        rpa_layout = QVBoxLayout()
        
        self.rpa_status_label = QLabel("No RPA script loaded")
        rpa_layout.addWidget(self.rpa_status_label)
        
        rpa_btn_layout = QHBoxLayout()
        create_rpa_btn = QPushButton("Create RPA Script")
        create_rpa_btn.clicked.connect(self.create_rpa_script)
        load_rpa_btn = QPushButton("Load RPA Script")
        load_rpa_btn.clicked.connect(self.load_rpa_script)
        clear_rpa_btn = QPushButton("Clear")
        clear_rpa_btn.clicked.connect(self.clear_rpa_script)
        rpa_btn_layout.addWidget(create_rpa_btn)
        rpa_btn_layout.addWidget(load_rpa_btn)
        rpa_btn_layout.addWidget(clear_rpa_btn)
        rpa_layout.addLayout(rpa_btn_layout)
        
        rpa_group.setLayout(rpa_layout)
        left_layout.addWidget(rpa_group)
        
        # Control buttons
        control_layout = QHBoxLayout()
        self.start_button = QPushButton("START SIMULATION")
        self.start_button.setMinimumHeight(50)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #555555;
            }
        """)
        self.start_button.clicked.connect(self.start_simulation)
        
        self.stop_button = QPushButton("STOP")
        self.stop_button.setMinimumHeight(50)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.stop_button.clicked.connect(self.stop_simulation)
        
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        left_layout.addLayout(control_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        left_layout.addWidget(self.progress_bar)
        
        # Stats
        stats_group = QGroupBox("Statistics")
        stats_layout = QVBoxLayout()
        
        self.stats_label = QLabel(f"User Agents Available: {get_user_agent_count():,}")
        stats_layout.addWidget(self.stats_label)
        
        self.status_label = QLabel("Status: Ready")
        stats_layout.addWidget(self.status_label)
        
        stats_group.setLayout(stats_layout)
        left_layout.addWidget(stats_group)
        
        left_layout.addStretch()
        
        # Right panel (Log)
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        log_group = QGroupBox("Activity Log")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        log_btn_layout = QHBoxLayout()
        clear_log_btn = QPushButton("Clear Log")
        clear_log_btn.clicked.connect(lambda: self.log_text.clear())
        export_log_btn = QPushButton("Export Log")
        export_log_btn.clicked.connect(self.export_log)
        log_btn_layout.addWidget(clear_log_btn)
        log_btn_layout.addWidget(export_log_btn)
        log_layout.addLayout(log_btn_layout)
        
        log_group.setLayout(log_layout)
        right_layout.addWidget(log_group)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)
        
        # Status bar
        self.statusBar().showMessage("Ready - HUMANEX Version 5")
    
    def log(self, message):
        """Add message to log"""
        self.log_text.append(message)
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def load_proxies(self):
        """Load proxies from text input"""
        proxy_text = self.proxy_text.toPlainText().strip()
        if not proxy_text:
            return
        
        proxies = [p.strip() for p in proxy_text.split('\n') if p.strip()]
        self.proxy_handler = ProxyHandler(proxies)
        
        count = self.proxy_handler.get_proxy_count()
        self.proxy_count_label.setText(f"Proxies loaded: {count}")
        self.log(f"Loaded {count} proxies")
    
    def create_rpa_script(self):
        """Open RPA script creator"""
        dialog = RPACreatorDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.rpa_script = dialog.get_script()
            self.rpa_status_label.setText(f"RPA Script: {self.rpa_script.name} ({len(self.rpa_script.actions)} actions)")
            self.log(f"RPA Script created: {self.rpa_script.name}")
    
    def load_rpa_script(self):
        """Load RPA script from file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load RPA Script", "", "JSON Files (*.json)"
        )
        if filename:
            try:
                self.rpa_script = RPAScript.load_from_file(filename)
                self.rpa_status_label.setText(f"RPA Script: {self.rpa_script.name} ({len(self.rpa_script.actions)} actions)")
                self.log(f"RPA Script loaded: {self.rpa_script.name}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not load script: {str(e)}")
    
    def clear_rpa_script(self):
        """Clear RPA script"""
        self.rpa_script = None
        self.rpa_status_label.setText("No RPA script loaded")
        self.log("RPA Script cleared")
    
    def start_simulation(self):
        """Start simulation"""
        url = self.url_input.text().strip()
        
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a target URL")
            return
        
        if not url.startswith(('http://', 'https://')):
            QMessageBox.warning(self, "Error", "URL must start with http:// or https://")
            return
        
        # Disable start button
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_label.setText("Status: Running")
        self.progress_bar.setValue(0)
        
        # Get configuration
        mode = self.mode_combo.currentText().lower().replace(' ', '_')
        if mode == "direct_visit":
            mode = "direct"
        elif mode == "search_traffic":
            mode = "search"
        elif mode == "referral_traffic":
            mode = "referral"
        
        platform = self.platform_combo.currentText().lower()
        if platform == "random":
            platform = None
        
        num_profiles = self.profiles_spin.value()
        
        self.log("\n" + "="*80)
        self.log(f"Starting {num_profiles} concurrent profile(s)")
        self.log("="*80)
        
        # Create workers for concurrent profiles
        for i in range(num_profiles):
            config = {
                'url': url,
                'traffic_mode': mode,
                'search_query': self.query_input.text(),
                'platform': platform,
                'stay_time': self.stay_time_spin.value(),
                'extra_pages': self.extra_pages_spin.value(),
                'proxy_handler': self.proxy_handler if self.proxy_handler.get_proxy_count() > 0 else None,
                'rpa_script': self.rpa_script,
                'profile_id': i + 1
            }
            
            worker = BrowserWorker(config)
            worker.log_signal.connect(lambda msg, pid=i+1: self.log(f"[Profile {pid}] {msg}"))
            worker.finished_signal.connect(self.simulation_finished)
            worker.progress_signal.connect(self.update_progress)
            
            self.active_workers.append(worker)
            worker.start()
            
            # Small delay between starting workers
            if i < num_profiles - 1:
                time.sleep(1)
    
    def stop_simulation(self):
        """Stop simulation"""
        self.log("Stopping all profiles...")
        
        for worker in self.active_workers:
            if worker.isRunning():
                worker.stop()
        
        self.stop_button.setEnabled(False)
    
    def simulation_finished(self, success, message):
        """Handle simulation completion"""
        # Check if all workers are finished
        all_finished = all(not w.isRunning() for w in self.active_workers)
        
        if all_finished:
            self.active_workers.clear()
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.status_label.setText("Status: Completed")
            self.progress_bar.setValue(100)
            self.statusBar().showMessage("All simulations completed")
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)
    
    def export_log(self):
        """Export log to file"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Log", "", "Text Files (*.txt)"
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.log_text.toPlainText())
                QMessageBox.information(self, "Success", "Log exported successfully")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not export log: {str(e)}")
    
    def closeEvent(self, event):
        """Handle application close"""
        for worker in self.active_workers:
            if worker.isRunning():
                worker.stop()
                worker.wait()
        event.accept()


def main():
    """Main application entry point"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = HumanexBotV5()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

# HUMANEX VERSION 5 - Technical Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         HUMANEX VERSION 5                            │
│                  Advanced Traffic Simulation Bot                     │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
            ┌───────▼───────┐           ┌────────▼────────┐
            │  Main GUI     │           │  Core Engine    │
            │  (PyQt5)      │           │  (Workers)      │
            └───────┬───────┘           └────────┬────────┘
                    │                            │
        ┌───────────┼────────────┐              │
        │           │            │              │
   ┌────▼────┐ ┌───▼────┐ ┌────▼────┐         │
   │ Config  │ │ Logs   │ │ Control │         │
   │ Panel   │ │ Panel  │ │ Buttons │         │
   └─────────┘ └────────┘ └─────────┘         │
                                               │
                    ┌──────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
   ┌────▼────┐ ┌───▼────┐ ┌───▼────┐
   │Worker 1 │ │Worker 2│ │Worker N│  (Up to 200)
   └────┬────┘ └───┬────┘ └───┬────┘
        │          │          │
   ┌────▼────┐ ┌──▼─────┐ ┌──▼─────┐
   │Browser 1│ │Browser2│ │BrowserN│
   └─────────┘ └────────┘ └────────┘
```

## Component Architecture

### 1. Main Application (humanex_v5.py)

```
HumanexBotV5 (QMainWindow)
├── GUI Components
│   ├── Left Panel (Configuration)
│   │   ├── Basic Settings
│   │   ├── Advanced Settings
│   │   ├── Proxy Configuration
│   │   └── RPA Settings
│   └── Right Panel (Logging)
│       ├── Activity Log
│       └── Control Buttons
├── Worker Management
│   ├── BrowserWorker threads
│   ├── Signal/Slot connections
│   └── Thread lifecycle
└── State Management
    ├── Configuration storage
    ├── Proxy handler
    └── RPA script
```

### 2. Browser Worker (BrowserWorker)

```
BrowserWorker (QThread)
├── Initialization
│   ├── Load configuration
│   ├── Select user agent
│   └── Configure proxy
├── Playwright Setup
│   ├── Launch browser
│   ├── Create context
│   └── Open page
├── Traffic Mode Execution
│   ├── Direct Visit
│   ├── Search Traffic
│   └── Referral Traffic
├── Interaction Engine
│   ├── Human-like scrolling
│   ├── Article clicking
│   ├── Text highlighting
│   └── Extra pages
├── RPA Execution
│   └── Run custom script
└── Cleanup
    ├── Close context
    └── Close browser
```

## Module Relationships

### Core Modules

```
humanex_v5.py (Main Application)
      │
      ├─> user_agents.py (User Agent Database)
      │   └── Provides random user agents by platform
      │
      ├─> proxy_handler.py (Proxy Management)
      │   ├── Parse multiple formats
      │   ├── Rotate proxies
      │   └── Generate Playwright configs
      │
      ├─> traffic_modes.py (Traffic Simulation)
      │   ├── DirectVisitMode
      │   ├── SearchTrafficMode
      │   └── ReferralTrafficMode
      │
      ├─> interactions.py (Interaction Engine)
      │   ├── Human-like scrolling
      │   ├── Click articles
      │   ├── Highlight text
      │   └── Mouse movements
      │
      └─> rpa_system.py (RPA Automation)
          ├── RPAScript
          ├── Action classes
          └── JSON import/export
```

### Data Flow

```
User Input → GUI → Configuration → Worker Thread → Playwright → Browser
                                         │
                                         ├─> User Agent Module
                                         ├─> Proxy Handler
                                         ├─> Traffic Mode
                                         ├─> Interaction Engine
                                         └─> RPA System
                                              │
Browser Actions → Logs → Signal → GUI → Activity Log Display
```

## Threading Model

### Main Thread (GUI)
- **Responsibility**: User interface, event handling
- **Components**: PyQt5 widgets, event loop
- **Communication**: Signal/Slot mechanism

### Worker Threads (Automation)
- **Responsibility**: Browser automation, interactions
- **Components**: Playwright, browser control
- **Communication**: Signals to main thread
- **Isolation**: Each worker independent

### Thread Safety
```
Main Thread              Worker Threads
    │                         │
    ├─ GUI Updates            ├─ Browser Control
    ├─ User Input             ├─ Page Interactions
    ├─ Config Changes         ├─ Network Requests
    │                         │
    ◄─── Signals ─────────────┤
    │   (log_signal)          │
    │   (progress_signal)     │
    │   (finished_signal)     │
```

## Traffic Mode Implementation

### Direct Visit Mode
```
1. Navigate to URL
2. Wait for page load
3. Initial pause (2-4s)
4. Human-like scrolling
5. Highlight text (optional)
6. Click articles (optional)
7. Open extra pages (optional)
8. Final pause (3-6s)
```

### Search Traffic Mode
```
1. Navigate to Google
2. Enter search query
3. Wait for results
4. Find target domain
5. Click result link
   ├─ Success: Continue with Direct Visit
   └─ Fail: Fallback to Direct Visit
```

### Referral Traffic Mode
```
1. Generate UTM parameters
   ├─ utm_source (social platform)
   ├─ utm_medium (traffic type)
   ├─ utm_campaign (campaign ID)
   ├─ utm_content (content ID)
   └─ utm_term (term ID)
2. Visit referrer (optional)
3. Navigate with UTM URL
4. Continue with Direct Visit
```

## RPA System Architecture

### Script Structure
```
RPAScript
├── Metadata
│   ├── Name
│   ├── Description
│   ├── Created timestamp
│   └── Modified timestamp
└── Actions (ordered list)
    ├── Action 1
    ├── Action 2
    └── Action N
```

### Action Types
```
NavigateAction    → page.goto(url)
ClickAction       → element.click()
InputAction       → element.type(text)
ScrollAction      → window.scrollBy()
WaitAction        → time.sleep()
SelectAction      → page.select_option()
HoverAction       → element.hover()
```

### Execution Flow
```
Load Script → Validate → Execute Actions → Log Results
                │                │
                └── JSON Parse   └── Try/Catch Error Handling
```

## Proxy System Architecture

### Proxy Formats Supported
```
1. ip:port
2. ip:port:username:password
3. username:password@ip:port
4. http://ip:port
5. http://username:password@ip:port
6. socks5://ip:port
7. socks5://username:password@ip:port
```

### Proxy Flow
```
Input → Parse → Validate → Store → Rotate → Apply to Browser
         │        │          │       │
         │        │          │       └─ Round-robin or random
         │        │          └─ Internal format
         │        └─ Format validation
         └─ String parsing
```

## User Agent System

### Generation Strategy
```
Platform Selection
    │
    ├─ Windows
    │   ├─ Chrome versions 100-122
    │   ├─ Edge versions 100-122
    │   └─ Firefox versions 100-122
    │
    ├─ Android
    │   ├─ Chrome on various devices
    │   ├─ Samsung Browser
    │   └─ Multiple Android versions (10-14)
    │
    └─ Random
        └─ Mix of above
```

### User Agent Components
```
Mozilla/5.0 (Platform; Device) Engine/Version Browser/Version
            └─────┬─────┘      └─────┬────┘  └──────┬──────┘
                  │                  │              │
              Platform          Engine Info    Browser Info
```

## Interaction Engine

### Human-like Behaviors
```
Scrolling Algorithm:
├── Random distance (50-300px)
├── Variable speed (0.3-1.2s)
├── Random intervals (0.5-2.5s)
└── Reading pauses (20% chance, 2-5s)

Clicking Algorithm:
├── Find article links
├── Filter by domain
├── Scroll to element
├── Wait (0.5-1.5s)
└── Click

Text Highlighting:
├── Find paragraphs
├── Scroll to view
├── Triple-click (select all)
└── Deselect after pause
```

## Error Handling Strategy

### Levels of Error Handling
```
1. Input Validation
   └── Pre-execution checks

2. Network Errors
   ├── Timeout handling
   └── Retry logic

3. Browser Errors
   ├── Element not found
   └── Navigation failures

4. Proxy Errors
   ├── Connection failures
   └── Authentication issues

5. System Errors
   ├── Resource exhaustion
   └── Thread failures
```

### Error Recovery
```
Error Detected → Log Error → Attempt Recovery → Continue or Fail Gracefully
                      │              │
                      │              ├─ Retry operation
                      │              ├─ Use fallback
                      │              └─ Skip and continue
                      │
                      └─ User notification via log
```

## Performance Optimization

### Resource Management
```
Browser Instances
├── Limit: 200 concurrent
├── Cleanup: Automatic on finish
└── Memory: Context isolation

Threading
├── Worker pool: Up to 200
├── Overhead: Minimal per thread
└── Coordination: Signal-based

Network
├── Wait strategy: networkidle
├── Timeout: 30 seconds
└── Retry: On specific errors
```

### Scalability Considerations
```
1-10 profiles:   Minimal resources
11-50 profiles:  Moderate resources (8GB RAM)
51-100 profiles: High resources (16GB RAM)
101-200 profiles: Enterprise resources (32GB+ RAM)
```

## Security & Privacy

### Data Protection
```
No Data Collection
├── No user data stored
├── No analytics sent
└── No telemetry

Local Execution
├── All operations local
├── No cloud dependencies
└── User has full control

Proxy Privacy
├── Optional proxy use
├── Multiple proxy support
└── No proxy data logged externally
```

### Responsible Design
```
Visible Operation
├── Non-headless browsers
└── User can see all actions

Manual Control
├── User must start
├── User can stop
└── Clear status indicators

Comprehensive Logging
├── All actions logged
├── Timestamps recorded
└── Audit trail available
```

## Testing Strategy

### Module Testing
```
test_modules.py
├── User Agents: Generation and selection
├── Proxy Handler: Parsing and rotation
├── Traffic Modes: Mode selection and setup
├── RPA System: Script creation and export
├── Interactions: Class imports
└── Main App: Import validation
```

### Integration Testing
```
Manual Testing
├── GUI functionality
├── Browser automation
├── Traffic simulation
├── RPA execution
└── Multi-profile concurrency
```

## Deployment Architecture

### Local Deployment (Default)
```
User's Machine
├── Python 3.7+
├── PyQt5
├── Playwright + Chromium
├── HUMANEX files
└── Configuration
```

### Requirements
```
System Requirements:
├── OS: Windows/Linux/Mac
├── RAM: 4GB minimum, 8GB+ recommended
├── CPU: Multi-core recommended
├── Display: For visible browsers
└── Network: Internet connection
```

---

**HUMANEX VERSION 5** - Robust, Scalable, Professional Architecture

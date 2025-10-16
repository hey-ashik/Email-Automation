# 📂 PROJECT STRUCTURE

```
Email-Automation-main/
│
├── 📄 app.py                    # Main Flask application (NEW)
│   ├── Routes for web dashboard
│   ├── API endpoints
│   └── File upload handling
│
├── 📄 main.py                   # Original CLI script (PRESERVED)
│   └── Still works independently!
│
├── 📄 utils.py                  # Email sending logic (NEW)
│   ├── send_single_email()
│   ├── send_bulk_emails()
│   ├── validate_excel_columns()
│   └── All original logic preserved
│
├── 📄 config_handler.py         # Configuration management (NEW)
│   ├── load_config()
│   ├── save_config()
│   └── Dynamic credential storage
│
├── 📄 config.json               # Email credentials (NEW)
│   ├── smtp_server
│   ├── smtp_port
│   ├── sender_email
│   ├── sender_password
│   └── sender_name
│
├── 📄 requirements.txt          # Python dependencies (UPDATED)
│   ├── pandas
│   ├── openpyxl
│   ├── flask
│   ├── werkzeug
│   ├── requests
│   ├── gspread
│   ├── oauth2client
│   └── python-dotenv
│
├── 📁 templates/                # HTML templates (NEW)
│   └── 📄 index.html           # Main dashboard UI
│       ├── Sidebar navigation
│       ├── Upload section
│       ├── Config section
│       ├── Send section
│       ├── Logs section
│       └── Instructions section
│
├── 📁 static/                   # Static assets (NEW)
│   ├── 📁 css/
│   │   └── 📄 style.css        # Dashboard styles
│   │       ├── Responsive design
│   │       ├── #E78A53 theme
│   │       └── ~950 lines
│   │
│   ├── 📁 js/
│   │   └── 📄 main.js          # Frontend logic
│   │       ├── File upload handling
│   │       ├── API calls
│   │       ├── Real-time updates
│   │       └── ~550 lines
│   │
│   └── 📁 uploads/             # Uploaded files
│       └── 📄 .gitkeep         # Keeps directory in git
│
├── 📄 .gitignore               # Git ignore rules (NEW)
│   ├── Protects config.json
│   ├── Protects uploads/
│   └── Protects sensitive data
│
├── 📄 README.md                # Full documentation (UPDATED)
│   ├── Features overview
│   ├── Installation guide
│   ├── Configuration steps
│   ├── Usage instructions
│   └── Troubleshooting
│
├── 📄 QUICKSTART.md            # Quick setup guide (NEW)
│   ├── 3-step setup
│   ├── Gmail App Password
│   └── First-time checklist
│
├── 📄 SETUP_GUIDE.md           # Complete guide (NEW)
│   ├── Detailed installation
│   ├── Configuration walkthrough
│   ├── Dashboard usage
│   ├── Troubleshooting
│   └── Advanced topics
│
├── 📄 PROJECT_SUMMARY.md       # Technical summary (NEW)
│   ├── What was built
│   ├── Features implemented
│   ├── API endpoints
│   └── Architecture overview
│
├── 📄 start.bat                # Windows launcher (NEW)
│   ├── Auto-creates venv
│   ├── Auto-installs dependencies
│   └── Starts Flask app
│
├── 📄 start.ps1                # PowerShell launcher (NEW)
│   └── Same as .bat but for PowerShell
│
├── 📄 data.xlsx                # Sample data file (EXISTING)
│   └── Your email list
│
└── 📁 venv/                    # Virtual environment
    └── (Created by you during setup)
```

---

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         WEB BROWSER                             │
│                    http://127.0.0.1:5000                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  index.html   │  ← Dashboard UI
                    │  + style.css  │
                    │  + main.js    │
                    └───────┬───────┘
                            │
                            │ API Calls (AJAX/Fetch)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                         FLASK APP (app.py)                       │
├─────────────────────────────────────────────────────────────────┤
│  Routes:                                                         │
│  • GET  /              → Render dashboard                       │
│  • POST /api/upload    → Upload Excel/CSV                       │
│  • POST /api/config    → Save email config                      │
│  • POST /api/send      → Start sending emails                   │
│  • GET  /api/status    → Get current status                     │
│  • GET  /api/logs      → Get email logs                         │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        │ Uses
                        ▼
        ┌───────────────────────────────────┐
        │         UTILS.PY                  │
        ├───────────────────────────────────┤
        │  • send_single_email()            │
        │  • send_bulk_emails()             │
        │  • validate_excel_columns()       │
        │  • Background threading           │
        └───────┬───────────────────────────┘
                │
                │ Reads config from
                ▼
        ┌───────────────────┐
        │  config.json      │
        ├───────────────────┤
        │  • sender_email   │
        │  • sender_password│
        │  • sender_name    │
        └───────┬───────────┘
                │
                │ Managed by
                ▼
        ┌───────────────────┐
        │ config_handler.py │
        ├───────────────────┤
        │  • load_config()  │
        │  • save_config()  │
        └───────────────────┘
```

---

## 🌐 Request Flow Example

### Example: Uploading and Sending Emails

```
1. User drags Excel file to dashboard
   ↓
2. JavaScript (main.js) catches drop event
   ↓
3. JavaScript sends POST to /api/upload
   ↓
4. Flask (app.py) receives file
   ↓
5. File saved to static/uploads/
   ↓
6. utils.py validates columns
   ↓
7. Preview data extracted with pandas
   ↓
8. JSON response sent back to browser
   ↓
9. JavaScript displays preview in UI
   ↓
10. User clicks "Start Sending"
    ↓
11. JavaScript sends POST to /api/send
    ↓
12. Flask starts background thread
    ↓
13. utils.py reads config.json
    ↓
14. For each row in Excel:
        - Load email data
        - Connect to SMTP server
        - Send email
        - Log result
    ↓
15. JavaScript polls /api/status every 2 seconds
    ↓
16. UI updates with:
        - Progress bar
        - Sent count
        - Failed count
        - Recent logs
    ↓
17. Complete! Logs displayed in Logs section
```

---

## 📡 API Endpoints Map

```
┌──────────────────────────────────────────────────────────────┐
│                      API ENDPOINTS                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  GET  /                                                      │
│  └─→ Serves dashboard (index.html)                          │
│                                                              │
│  GET  /api/config                                            │
│  └─→ Returns current email configuration                    │
│      (without password for security)                        │
│                                                              │
│  POST /api/config                                            │
│  └─→ Updates email configuration                            │
│      Body: {sender_email, sender_password, sender_name...}  │
│                                                              │
│  POST /api/upload                                            │
│  └─→ Handles Excel/CSV file upload                          │
│      Returns: {success, filename, filepath, preview}        │
│                                                              │
│  POST /api/google-sheet                                      │
│  └─→ Imports data from Google Sheets                        │
│      Body: {url}                                            │
│      Returns: {success, filename, preview}                  │
│                                                              │
│  POST /api/send                                              │
│  └─→ Starts email sending process                           │
│      Body: {filepath, sender_name}                          │
│      Spawns background thread                               │
│                                                              │
│  POST /api/stop                                              │
│  └─→ Stops email sending                                    │
│      Sets global stop flag                                  │
│                                                              │
│  GET  /api/status                                            │
│  └─→ Returns current sending status                         │
│      Returns: {is_sending, total_logs, recent_logs}         │
│                                                              │
│  GET  /api/logs                                              │
│  └─→ Returns all email logs                                 │
│      Returns: {success, logs[]}                             │
│                                                              │
│  POST /api/logs/clear                                        │
│  └─→ Clears all logs                                        │
│      Resets in-memory log array                             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🎨 UI Component Hierarchy

```
Dashboard (index.html)
│
├── Sidebar
│   ├── Header
│   │   ├── Logo/Title
│   │   └── Close Button (mobile)
│   └── Navigation Menu
│       ├── Upload Data
│       ├── Email Config
│       ├── Send Emails
│       ├── Logs
│       └── Instructions
│
├── Overlay (mobile backdrop)
│
└── Main Content
    ├── Top Bar
    │   ├── Menu Toggle (mobile)
    │   ├── Page Title
    │   └── Status Indicator
    │
    └── Content Sections
        │
        ├── Upload Section
        │   ├── Excel Upload Card
        │   │   ├── Drag & Drop Area
        │   │   ├── File Preview
        │   │   └── Data Table Preview
        │   └── Google Sheets Card
        │       ├── URL Input
        │       ├── Load Button
        │       └── Sheet Preview
        │
        ├── Config Section
        │   ├── Configuration Form
        │   │   ├── Sender Name
        │   │   ├── Sender Email
        │   │   ├── App Password
        │   │   ├── SMTP Server
        │   │   └── SMTP Port
        │   └── Help Card
        │       └── Gmail App Password Guide
        │
        ├── Send Section
        │   ├── Status Cards Grid
        │   │   ├── Data Source Info
        │   │   ├── Total Emails
        │   │   ├── Sent Count
        │   │   └── Failed Count
        │   ├── Control Buttons
        │   │   ├── Start Sending
        │   │   └── Stop Sending
        │   └── Progress Bar
        │
        ├── Logs Section
        │   └── Logs Card
        │       ├── Clear Logs Button
        │       └── Log Entries
        │           ├── Timestamp
        │           ├── Recipient
        │           ├── Subject
        │           └── Status
        │
        └── Instructions Section
            ├── Excel Format Card
            ├── Example Data Card
            ├── Security Tips Card
            └── Getting Started Card
```

---

## 🔐 Security Layers

```
┌────────────────────────────────────────────────────────────┐
│                    SECURITY MEASURES                       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Configuration                                          │
│     • config.json in .gitignore                           │
│     • Password not sent to frontend                       │
│     • App Password requirement (not regular password)     │
│                                                            │
│  2. File Upload                                            │
│     • File type validation (.xlsx, .xls, .csv only)       │
│     • File size limit (16MB max)                          │
│     • Secure filename sanitization                        │
│     • Uploads directory in .gitignore                     │
│                                                            │
│  3. Data Validation                                        │
│     • Email address format checking                       │
│     • Required field validation                           │
│     • Column existence verification                       │
│     • Input sanitization                                  │
│                                                            │
│  4. Network Security                                       │
│     • STARTTLS encryption for SMTP                        │
│     • Local-only by default (0.0.0.0 binding)            │
│     • No external data transmission                       │
│     • All processing on local machine                     │
│                                                            │
│  5. Error Handling                                         │
│     • Try-catch blocks everywhere                         │
│     • Detailed logging for debugging                      │
│     • User-friendly error messages                        │
│     • Graceful failure handling                           │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 📈 Scalability Considerations

```
Current Implementation:
• In-memory log storage
• Single-threaded email sending
• Local file storage
• No database

Suitable For:
✅ Personal use
✅ Small teams (< 10 users)
✅ Batch sizes < 1,000 emails
✅ Occasional sending

Future Enhancements (if needed):
📊 Database integration (SQLite/PostgreSQL)
🔄 Multi-threaded sending
📤 Queue system (Celery/RQ)
☁️ Cloud storage integration
👥 Multi-user authentication
📊 Analytics dashboard
🔔 Webhook notifications
```

---

## 🎯 Component Responsibilities

```
┌─────────────────────────────────────────────────────────────┐
│  FILE              │  RESPONSIBILITY                         │
├────────────────────┼─────────────────────────────────────────┤
│  app.py            │  • Flask app initialization             │
│                    │  • Route definitions                    │
│                    │  • Request/response handling            │
│                    │  • API endpoints                        │
│                    │  • File upload processing               │
├────────────────────┼─────────────────────────────────────────┤
│  utils.py          │  • Email sending logic                  │
│                    │  • SMTP connection                      │
│                    │  • Excel/CSV parsing                    │
│                    │  • Background threading                 │
│                    │  • Log management                       │
├────────────────────┼─────────────────────────────────────────┤
│  config_handler.py │  • Configuration loading                │
│                    │  • Configuration saving                 │
│                    │  • JSON file operations                 │
├────────────────────┼─────────────────────────────────────────┤
│  index.html        │  • UI structure                         │
│                    │  • Layout definition                    │
│                    │  • Template rendering                   │
├────────────────────┼─────────────────────────────────────────┤
│  style.css         │  • Visual styling                       │
│                    │  • Responsive design                    │
│                    │  • Animations                           │
│                    │  • Theme colors                         │
├────────────────────┼─────────────────────────────────────────┤
│  main.js           │  • User interactions                    │
│                    │  • API communication                    │
│                    │  • DOM manipulation                     │
│                    │  • Real-time updates                    │
│                    │  • Form validation                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 State Management

```
Frontend State (JavaScript):
• currentFile - Path to uploaded file
• statusCheckInterval - Polling timer
• Form field values (sender info)

Backend State (Python):
• email_logs - Array of log entries
• is_sending - Boolean sending flag
• should_stop - Boolean stop flag
• config.json - Persistent configuration

Session State:
• No user sessions (single-user app)
• No cookies required
• No authentication needed
```

---

**This structure ensures:**
- ✅ Clean separation of concerns
- ✅ Easy maintenance
- ✅ Modular architecture
- ✅ Scalable design
- ✅ Security best practices


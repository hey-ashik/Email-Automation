# 🎯 COMPLETE SETUP & USAGE GUIDE

## 📋 Table of Contents
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Running the Application](#running-the-application)
4. [Using the Dashboard](#using-the-dashboard)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Usage](#advanced-usage)

---

## 🔧 Installation

### Method 1: Automatic Setup (Easiest)

**Windows Command Prompt:**
```cmd
start.bat
```

**Windows PowerShell:**
```powershell
.\start.ps1
```

These scripts will automatically:
- Create virtual environment
- Install all dependencies
- Start the application

### Method 2: Manual Setup

#### Step 1: Create Virtual Environment
```powershell
python -m venv venv
```

#### Step 2: Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` appear in your terminal.

#### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- pandas (data processing)
- openpyxl (Excel files)
- requests (HTTP requests)
- gspread (Google Sheets)
- and more...

---

## ⚙️ Configuration

### 1. Gmail App Password Setup

**Why App Password?**
Gmail doesn't allow apps to use your regular password for security reasons. You need a special 16-character "App Password".

**How to Get It:**

1. **Go to Google Account Settings**
   - Visit: https://myaccount.google.com/security

2. **Enable 2-Step Verification**
   - If not already enabled, you must enable it first
   - Follow the prompts to set up 2FA

3. **Generate App Password**
   - Scroll down to "App passwords" section
   - Click on it (you may need to re-enter your password)
   - Select app: **Mail**
   - Select device: **Windows Computer** (or other)
   - Click **Generate**

4. **Copy the Password**
   - You'll see a 16-character password like: `abcd efgh ijkl mnop`
   - Copy this password (spaces don't matter)
   - You won't be able to see it again!

5. **Save It Securely**
   - You'll enter this in the dashboard
   - It will be saved in `config.json`

### 2. Prepare Your Email Data

Create an Excel or CSV file with these columns:

**Required Columns:**
- `To` - Recipient email address
- `Subject` - Email subject line
- `Body` - Email message content

**Optional Columns:**
- `CC` - Carbon copy email addresses
- `BCC` - Blind carbon copy email addresses
- `Attachment` - Full path to attachment file

**Example:**

| To | Subject | Body | CC |
|----|---------|------|----|
| john@example.com | Meeting Reminder | Hi John, don't forget our meeting tomorrow at 10 AM. | manager@example.com |
| sarah@example.com | Project Update | Hi Sarah, here's the latest update on the project. | |

**Save as:** `emails.xlsx` or `emails.csv`

---

## 🚀 Running the Application

### Option 1: Use Startup Scripts

**Windows:**
```cmd
start.bat
```

**PowerShell:**
```powershell
.\start.ps1
```

### Option 2: Manual Start

```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Run the application
python app.py
```

### What You'll See

```
============================================================
🚀 Email Automation Dashboard Started
============================================================
📧 Access the dashboard at: http://127.0.0.1:5000
============================================================
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### Access the Dashboard

Open your web browser and go to:
```
http://127.0.0.1:5000
```
or
```
http://localhost:5000
```

---

## 📱 Using the Dashboard

### Navigation

The left sidebar contains 5 main sections:
1. 📂 Upload Data
2. ⚙️ Email Config
3. ✉️ Send Emails
4. 🧾 Logs
5. ℹ️ Instructions

### 1. Upload Data Section

**Upload Excel/CSV File:**
1. Click "Choose File" or drag & drop your file
2. File will be validated automatically
3. Preview of data will be shown
4. If validation fails, you'll see which columns are missing

**Connect Google Sheets:**
1. Make your Google Sheet publicly accessible:
   - Open your Google Sheet
   - Click "Share" button
   - Change to "Anyone with the link can view"
   - Copy the share link
2. Paste the link in the dashboard
3. Click "Load Sheet"
4. Data will be imported and previewed

### 2. Email Config Section

**Configure Your Email:**
1. **Sender Name**: How you want to appear to recipients
   - Example: "John Doe" or "Marketing Team"
   
2. **Sender Email**: Your Gmail address
   - Example: yourname@gmail.com
   
3. **App Password**: The 16-character password from Google
   - Paste without spaces: `abcdefghijklmnop`
   - Or with spaces: `abcd efgh ijkl mnop` (both work)
   
4. **SMTP Server**: Leave as `smtp.gmail.com`
   
5. **SMTP Port**: Leave as `587`

6. Click "Save Configuration"

**Your credentials are saved in `config.json` and automatically loaded next time!**

### 3. Send Emails Section

**Before Sending:**
- Make sure you've uploaded data
- Make sure you've configured email settings
- Review the "Total Emails" count

**To Send:**
1. Click "Start Sending"
2. Watch the progress bar
3. Monitor sent/failed counts in real-time
4. Status indicator at top shows current state

**To Stop:**
- Click "Stop Sending" at any time
- Current email will complete, then stop
- Check logs for what was sent

### 4. Logs Section

**View Logs:**
- Click "Logs" in sidebar
- See all sent emails with:
  - Recipient email
  - Subject
  - Status (Sent/Failed)
  - Timestamp
  - Error message (if failed)

**Clear Logs:**
- Click "Clear Logs" button
- Confirms before clearing
- Resets all counters

### 5. Instructions Section

- Complete documentation in the dashboard
- Excel format requirements
- Example data table
- Security tips
- Step-by-step guides

---

## 🔍 Troubleshooting

### Problem: Can't activate virtual environment

**Error:** `cannot be loaded because running scripts is disabled`

**Solution:**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again:
```powershell
.\venv\Scripts\Activate.ps1
```

---

### Problem: "No module named flask" or similar import errors

**Solution:**
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Problem: "535 Authentication failed" or login error

**Causes:**
- Using regular Gmail password (won't work!)
- App Password not generated correctly
- 2-Factor Authentication not enabled

**Solution:**
1. Enable 2FA on your Google account
2. Generate a new App Password
3. Copy the EXACT 16-character password
4. Enter it in Email Config section (spaces don't matter)
5. Click Save Configuration
6. Try sending again

---

### Problem: File upload fails - "Missing required columns"

**Solution:**
Make sure your Excel/CSV has these exact column names (case-sensitive):
- `To` (not "Email" or "to")
- `Subject` (not "subject")
- `Body` (not "Message" or "body")

Rename your columns in Excel if needed.

---

### Problem: Google Sheet won't load

**Causes:**
- Sheet is not publicly accessible
- Wrong link format

**Solution:**
1. Open your Google Sheet
2. Click "Share" → "Change to anyone with the link"
3. Copy the share link (not the edit link)
4. Paste in dashboard
5. Try again

---

### Problem: Attachment not found

**Error:** "Attachment not found: C:\path\to\file.pdf"

**Solution:**
- Use full absolute paths in your Excel file
- Example: `C:\Users\YourName\Documents\file.pdf`
- Make sure file exists at that exact location
- Use forward slashes `/` or double backslashes `\\`
  - Good: `C:/Users/Name/file.pdf`
  - Good: `C:\\Users\\Name\\file.pdf`
  - Bad: `C:\Users\Name\file.pdf` (might fail)

---

### Problem: Dashboard won't load / Connection refused

**Check:**
1. Is Flask running? (check terminal)
2. See any errors in terminal?
3. Try: http://localhost:5000 instead of 127.0.0.1
4. Check if port 5000 is already in use

**Solution:**
```powershell
# Stop the app (Ctrl+C)
# Start again
python app.py
```

---

### Problem: Browser shows "This site can't be reached"

**Solution:**
1. Check Flask is running (terminal should show "Running on...")
2. Make sure you're using the correct URL:
   - http://127.0.0.1:5000 or
   - http://localhost:5000
3. Try a different browser
4. Disable VPN if using one

---

## 🎓 Advanced Usage

### Using the Original CLI Version

The original `main.py` still works independently:

```powershell
# Make sure data.xlsx exists in the same directory
python main.py
```

This bypasses the dashboard and runs the original script.

---

### Custom SMTP Server (Non-Gmail)

If using a different email provider:

1. Go to Email Config section
2. Change SMTP Server (e.g., `smtp.outlook.com`, `smtp.yahoo.com`)
3. Change SMTP Port (e.g., 587, 465, 25)
4. Use your provider's app password
5. Save configuration

---

### Batch Processing Tips

**For Large Lists:**
1. Test with 5-10 emails first
2. Check logs for any errors
3. Fix any issues
4. Then send to full list

**Gmail Limits:**
- Free Gmail: ~500 emails per day
- Google Workspace: ~2,000 emails per day
- Spread sending across multiple days if needed

---

### Backup Configuration

Your config is saved in `config.json`:
```powershell
# Copy to backup
copy config.json config.backup.json
```

---

### Running on Network

To access from other devices on your network:

1. Find your computer's IP address:
```powershell
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.100)

2. The app already runs on 0.0.0.0, so just access:
```
http://YOUR_IP:5000
```
Example: http://192.168.1.100:5000

---

### Scheduling Automated Sends

Use Windows Task Scheduler to run at specific times:

1. Create a batch file `auto_send.bat`:
```batch
@echo off
cd /d "C:\path\to\Email-Automation-main"
call venv\Scripts\activate.bat
python main.py
```

2. Open Task Scheduler
3. Create Basic Task
4. Set schedule (daily, weekly, etc.)
5. Action: Start a program
6. Program: Path to your `auto_send.bat`

---

## 📊 Data Privacy & Security

### What Gets Stored?

**Locally on Your Computer:**
- `config.json` - Your email credentials
- `static/uploads/` - Uploaded Excel/CSV files
- In-memory logs (cleared when app stops)

**Not Stored Anywhere:**
- No cloud services
- No external databases
- No tracking
- All data stays on your machine

### Protect Your Data

1. **Add to `.gitignore`** (already done):
   - config.json
   - *.xlsx
   - *.csv
   - static/uploads/

2. **Don't share:**
   - Your config.json file
   - Your App Password
   - Files with email addresses

3. **Secure your computer:**
   - Use strong password
   - Enable BitLocker if available
   - Regular backups

---

## 🎉 Success Checklist

Before first use, verify:

- [ ] Virtual environment created and activated
- [ ] All dependencies installed (no import errors)
- [ ] Gmail App Password generated
- [ ] 2-Factor Authentication enabled on Gmail
- [ ] Excel file prepared with correct columns
- [ ] Config saved in dashboard
- [ ] Test email sent to yourself successfully

Once all checked, you're ready to go! 🚀

---

## 📞 Support

**For Issues:**
1. Check this guide first
2. Review error messages carefully
3. Check logs in dashboard
4. Verify configuration
5. Test with simple data first

**Common Resources:**
- README.md - Full documentation
- QUICKSTART.md - Quick setup
- PROJECT_SUMMARY.md - Technical details
- Instructions section in dashboard

---

## 🌟 Tips for Success

1. **Always test first** - Send to yourself before bulk sending
2. **Start small** - Begin with 5-10 emails, not 500
3. **Check logs** - Review after each batch
4. **Personalize** - Use sender names for better engagement
5. **Respect limits** - Don't exceed Gmail's sending limits
6. **Be professional** - Follow email best practices
7. **Backup data** - Keep copies of your lists
8. **Monitor spam** - Check if emails go to spam folder

---

**Happy Emailing! 📧✨**

*Made with Python, Flask, and ❤️*

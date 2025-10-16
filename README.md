# Email Automation Dashboard

A modern, fully responsive Flask-based web application for automated email sending. Send bulk emails from Excel files or Google Sheets with an intuitive dashboard interface.

## 🌟 Features

- **Modern Web Dashboard UI** - Beautiful, responsive interface with sidebar navigation
- **Multiple Data Sources** - Upload Excel/CSV files or connect to Google Sheets
- **Dynamic Email Configuration** - Manage sender credentials through the UI
- **Custom Sender Names** - Personalize how your emails appear to recipients
- **Real-time Progress Tracking** - Monitor email sending status live
- **Detailed Logs** - View success/failure status for each email
- **Mobile Responsive** - Works perfectly on desktop, tablet, and mobile devices
- **Professional Design** - Clean interface with #E78A53 accent color

## 📋 Prerequisites

- Python 3.9 or higher
- Gmail account with App Password enabled
- Excel file with email data OR Google Sheets public link

## 🚀 Installation

### 1. Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

## ▶️ Running the Application

### Start the Flask Dashboard

```powershell
python app.py
```

The dashboard will be available at: **http://127.0.0.1:5000**

### Alternative: Run Original CLI Version

If you want to use the original command-line version:

```powershell
python main.py
```

## 📊 Data File Format

Your Excel/CSV file must contain these columns:

| Column | Required | Description |
|--------|----------|-------------|
| **To** | ✅ Yes | Recipient email address |
| **Subject** | ✅ Yes | Email subject line |
| **Body** | ✅ Yes | Email message content |
| **CC** | ❌ Optional | Carbon copy recipients |
| **BCC** | ❌ Optional | Blind carbon copy recipients |
| **Attachment** | ❌ Optional | File path to attachment |

### Example Data

| To | Subject | Body | CC |
|----|---------|------|-----|
| john@example.com | Hello John | This is a test email | jane@example.com |
| jane@example.com | Hello Jane | Another test message | |

## 🔧 Configuration

### Gmail App Password Setup

1. Go to your Google Account settings
2. Navigate to **Security** → **2-Step Verification**
3. Scroll down to **App passwords**
4. Generate a new app password for "Mail"
5. Copy the 16-character password
6. Enter it in the Email Configuration section of the dashboard

### Dashboard Configuration

1. Navigate to **Email Config** section
2. Enter your details:
   - **Sender Name**: Your name (appears to recipients)
   - **Sender Email**: Your Gmail address
   - **App Password**: The 16-character password from Google
   - **SMTP Server**: smtp.gmail.com (default)
   - **SMTP Port**: 587 (default)
3. Click **Save Configuration**

## 📁 Project Structure

```
Email-Automation-main/
├── app.py                  # Flask application entry point
├── main.py                 # Original CLI version (still works!)
├── utils.py                # Email sending logic
├── config_handler.py       # Configuration management
├── config.json             # Dynamic email credentials
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/
│   └── index.html         # Dashboard UI
├── static/
│   ├── css/
│   │   └── style.css      # Dashboard styles
│   ├── js/
│   │   └── main.js        # Frontend logic
│   └── uploads/           # Uploaded files directory
└── data.xlsx              # Your email data (optional)
```

## 🎨 Dashboard Sections

### 1. Upload Data
- Upload Excel/CSV files via drag & drop or file browser
- Connect to public Google Sheets
- Preview data before sending

### 2. Email Configuration
- Set sender name, email, and credentials
- Configure SMTP settings
- Test connection

### 3. Send Emails
- View sending status and progress
- Start/stop email campaigns
- Track sent/failed counts in real-time

### 4. Logs
- Detailed history of all sent emails
- Filter by success/failure status
- Clear logs when needed

### 5. Instructions
- Complete setup guide
- Data format requirements
- Security tips and best practices

## 🔒 Security Notes

- ⚠️ **Never use your actual Gmail password** - Always use App Passwords
- 🔐 Enable 2-Factor Authentication on your Google account
- 🤫 Keep your `config.json` private (add to .gitignore if using Git)
- ✅ Test with small batches before sending to large lists
- 📊 Respect Gmail's sending limits (~500 emails per day)

## 🛠️ Troubleshooting

### "Import could not be resolved" errors
These are just IDE warnings. Run `pip install -r requirements.txt` to install packages.

### "Login failed" error
- Verify you're using an App Password, not your regular password
- Make sure 2-Factor Authentication is enabled
- Check that your Gmail address is correct

### File upload fails
- Ensure file has required columns: To, Subject, Body
- Check file size is under 16MB
- Verify file format is .xlsx, .xls, or .csv

### Google Sheets not loading
- Make sure the sheet is publicly accessible
- Use the share link, not the edit link
- Check your internet connection

## 🚦 API Endpoints

The Flask backend provides these API endpoints:

- `GET /` - Dashboard UI
- `GET /api/config` - Get current configuration
- `POST /api/config` - Update configuration
- `POST /api/upload` - Upload Excel/CSV file
- `POST /api/google-sheet` - Load Google Sheet
- `POST /api/send` - Start sending emails
- `POST /api/stop` - Stop sending emails
- `GET /api/status` - Get sending status
- `GET /api/logs` - Get all logs
- `POST /api/logs/clear` - Clear logs

## 📝 Development Notes

### Key Features Preserved from Original
- ✅ All email sending logic intact from `main.py`
- ✅ Excel parsing with pandas
- ✅ SMTP authentication with Gmail
- ✅ Attachment handling
- ✅ Field validation and cleaning
- ✅ Error handling and logging

### New Features Added
- 🌐 Flask web framework integration
- 🎨 Modern responsive UI
- 📤 File upload handling
- 🔗 Google Sheets integration
- 🔄 Real-time status updates
- 📊 Visual progress tracking
- 🗂️ Persistent configuration storage

## 🤝 Support

For issues or questions:
1. Check the Instructions section in the dashboard
2. Review this README
3. Verify your Gmail App Password setup
4. Test with a small sample file first

## 📜 License

This project is for educational and personal use.

---

**Made with ❤️ using Flask, Python, and #E78A53**

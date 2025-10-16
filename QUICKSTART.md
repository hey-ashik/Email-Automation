# 🚀 Quick Start Guide

## Get Started in 3 Steps

### Step 1: Setup Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run the Application
```powershell
# Start the Flask dashboard
python app.py
```

### Step 3: Access Dashboard
Open your browser and go to: **http://127.0.0.1:5000**

---

## 📋 Checklist

Before sending emails, make sure you have:

- [ ] Created a virtual environment and installed dependencies
- [ ] Prepared an Excel/CSV file with required columns (To, Subject, Body)
- [ ] Obtained a Gmail App Password (NOT your regular password)
- [ ] Configured email settings in the dashboard
- [ ] Tested with a small sample first

---

## 🔑 Gmail App Password Setup

1. Go to https://myaccount.google.com/security
2. Enable **2-Step Verification** if not already enabled
3. Go to **App passwords** section
4. Select **Mail** and generate password
5. Copy the 16-character password (format: xxxx xxxx xxxx xxxx)
6. Enter it in the dashboard's Email Configuration section

---

## 📊 Excel File Format

Your file MUST have these columns:

| Column | Required | Example |
|--------|----------|---------|
| To | ✅ Yes | john@example.com |
| Subject | ✅ Yes | Hello John |
| Body | ✅ Yes | This is the email message |
| CC | ❌ Optional | jane@example.com |
| BCC | ❌ Optional | manager@example.com |
| Attachment | ❌ Optional | C:\files\document.pdf |

---

## 🎯 First Time Users

### Test with Sample Data

Create a simple Excel file with:
- Your own email in the "To" column
- A test subject
- A simple message

Send to yourself first to verify everything works!

---

## 🆘 Common Issues

### Issue: "No module named flask"
**Solution:** Run `pip install -r requirements.txt`

### Issue: "Login failed"
**Solution:** Use App Password, not your regular Gmail password

### Issue: "Missing columns"
**Solution:** Ensure Excel file has To, Subject, Body columns

---

## 🌐 Dashboard Navigation

1. **Upload Data** - Upload Excel or connect Google Sheets
2. **Email Config** - Set your sender credentials
3. **Send Emails** - Start your campaign
4. **Logs** - View sending history
5. **Instructions** - Complete documentation

---

## 📞 Need Help?

Check the full README.md for detailed documentation!

**Happy Emailing! 📧**

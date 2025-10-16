"""
Email Utility Module
Contains all email sending logic from the original main.py
Preserves exact functionality while making it reusable for Flask
"""
import smtplib
import pandas as pd
from email.message import EmailMessage
import os
import mimetypes
from config_handler import load_config
import threading
import time

# Global variables for tracking email sending status
email_logs = []
is_sending = False
should_stop = False
total_emails = 0
sent_count = 0
failed_count = 0
current_data_file = None

def clean_field(value):
    """Clean and validate field values"""
    if pd.isna(value):
        return ""
    return str(value).strip()

def send_single_email(to, cc="", bcc="", subject="", body="", attachment=None, sender_name=""):
    """
    Send a single email using SMTP
    This preserves the exact logic from original main.py
    """
    global email_logs, sent_count, failed_count
    
    # Load configuration dynamically
    config = load_config()
    SMTP_SERVER = config.get("smtp_server", "smtp.gmail.com")
    SMTP_PORT = config.get("smtp_port", 587)
    SENDER_EMAIL = config.get("sender_email", "")
    SENDER_PASSWORD = config.get("sender_password", "")
    
    if not sender_name:
        sender_name = config.get("sender_name", "")
    
    msg = EmailMessage()
    
    # Set sender with name if provided
    if sender_name:
        msg["From"] = f"{sender_name} <{SENDER_EMAIL}>"
    else:
        msg["From"] = SENDER_EMAIL

    to = clean_field(to)
    cc = clean_field(cc)
    bcc = clean_field(bcc)
    subject = clean_field(subject)

    if not to:
        log_entry = {
            "to": "N/A",
            "subject": subject,
            "status": "Failed",
            "message": "Missing 'To' address",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        email_logs.append(log_entry)
        print("Skipped: Missing 'To' address.")
        return False

    msg["To"] = to
    if cc:
        msg["Cc"] = cc
    if bcc:
        msg["Bcc"] = bcc
    msg["Subject"] = subject
    msg.set_content(str(body))

    # Handle attachments
    if attachment and not pd.isna(attachment):
        attachment_path = str(attachment).strip()
        if os.path.exists(attachment_path):
            mime_type, _ = mimetypes.guess_type(attachment_path)
            main_type, sub_type = (mime_type.split('/', 1)
                                   if mime_type else ('application', 'octet-stream'))
            with open(attachment_path, 'rb') as f:
                msg.add_attachment(f.read(),
                                   maintype=main_type,
                                   subtype=sub_type,
                                   filename=os.path.basename(attachment_path))
        else:
            log_entry = {
                "to": to,
                "subject": subject,
                "status": "Warning",
                "message": f"Attachment not found: {attachment_path}",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            email_logs.append(log_entry)
            print(f"Attachment not found: {attachment_path}")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
            
            log_entry = {
                "to": to,
                "subject": subject,
                "status": "Sent",
                "message": "Email sent successfully",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            email_logs.append(log_entry)
            sent_count += 1
            print(f"Email sent successfully to: {to}")
            return True
            
    except Exception as e:
        log_entry = {
            "to": to,
            "subject": subject,
            "status": "Failed",
            "message": str(e),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        email_logs.append(log_entry)
        failed_count += 1
        print(f"Failed to send to {to}: {e}")
        return False

def send_bulk_emails(data_file_path, sender_name=""):
    """
    Send bulk emails from Excel/CSV file
    This is the main automation function from original main.py
    """
    global is_sending, should_stop, email_logs, total_emails, sent_count, failed_count, current_data_file
    
    is_sending = True
    should_stop = False
    sent_count = 0
    failed_count = 0
    current_data_file = data_file_path
    
    try:
        # Read the data file
        if data_file_path.endswith('.csv'):
            data = pd.read_csv(data_file_path)
        else:
            data = pd.read_excel(data_file_path)
        
        # Set total emails count
        total_emails = len(data)
        
        # Send emails row by row
        for index, row in data.iterrows():
            if should_stop:
                log_entry = {
                    "to": "N/A",
                    "subject": "Bulk Send",
                    "status": "Stopped",
                    "message": f"Email sending stopped by user at {sent_count + failed_count}/{total_emails}",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                email_logs.append(log_entry)
                break
                
            send_single_email(
                to=row.get("To", ""),
                cc=row.get("CC", ""),
                bcc=row.get("BCC", ""),
                subject=row.get("Subject", ""),
                body=row.get("Body", ""),
                attachment=row.get("Attachment", ""),
                sender_name=sender_name
            )
            
            # Small delay to avoid rate limiting
            time.sleep(1)
        
        # Auto-stop when all emails are sent
        is_sending = False
        
        # Add completion log
        if not should_stop:
            log_entry = {
                "to": "N/A",
                "subject": "Bulk Send Complete",
                "status": "Sent",
                "message": f"Completed: {sent_count} sent, {failed_count} failed out of {total_emails} total",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            email_logs.append(log_entry)
        
        return True
        
    except Exception as e:
        log_entry = {
            "to": "N/A",
            "subject": "Bulk Send",
            "status": "Failed",
            "message": f"Error reading file: {str(e)}",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        email_logs.append(log_entry)
        is_sending = False
        return False

def send_bulk_emails_async(data_file_path, sender_name=""):
    """
    Send bulk emails in background thread to avoid blocking Flask
    """
    thread = threading.Thread(target=send_bulk_emails, args=(data_file_path, sender_name))
    thread.daemon = True
    thread.start()
    return thread

def stop_sending():
    """Stop the email sending process"""
    global should_stop
    should_stop = True

def get_sending_status():
    """Get current sending status"""
    return {
        "is_sending": is_sending,
        "should_stop": should_stop,
        "total_emails": total_emails,
        "sent_count": sent_count,
        "failed_count": failed_count
    }

def get_email_logs():
    """Get all email logs"""
    return email_logs

def clear_email_logs():
    """Clear all email logs"""
    global email_logs, sent_count, failed_count
    email_logs = []
    sent_count = 0
    failed_count = 0
    return True

def get_file_email_count(file_path):
    """Get total number of emails in a file"""
    try:
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        else:
            data = pd.read_excel(file_path)
        return len(data)
    except Exception as e:
        return 0

def validate_excel_columns(file_path):
    """
    Validate that the Excel/CSV file has required columns
    Returns (is_valid, missing_columns, preview_data)
    """
    required_columns = ["To", "Subject", "Body"]
    optional_columns = ["CC", "BCC", "Attachment"]
    
    try:
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        else:
            data = pd.read_excel(file_path)
        
        columns = data.columns.tolist()
        missing = [col for col in required_columns if col not in columns]
        
        # Get preview (first 5 rows) and replace NaN with empty string
        preview_data = data.head(5).fillna('').to_dict('records')
        
        # Clean the preview data to ensure JSON serialization
        preview = []
        for row in preview_data:
            clean_row = {}
            for key, value in row.items():
                # Convert all values to strings and handle NaN
                if pd.isna(value) or value == '':
                    clean_row[key] = ''
                else:
                    clean_row[key] = str(value)
            preview.append(clean_row)
        
        if missing:
            return False, missing, preview
        else:
            return True, [], preview
            
    except Exception as e:
        return False, [f"Error: {str(e)}"], []

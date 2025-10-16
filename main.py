import smtplib
import pandas as pd
from email.message import EmailMessage
import os
import mimetypes

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "ashikulislam2070@gmail.com"
SENDER_PASSWORD = "srao nyrz zyfk dnoq" 

data = pd.read_excel("data.xlsx")

def clean_field(value):
    if pd.isna(value):
        return ""
    return str(value).strip()

def send_email(to, cc="", bcc="", subject="", body="", attachment=None):
    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL

    to = clean_field(to)
    cc = clean_field(cc)
    bcc = clean_field(bcc)
    subject = clean_field(subject)

    if not to:
        print("Skipped: Missing 'To' address.")
        return

    msg["To"] = to
    if cc:
        msg["Cc"] = cc
    if bcc:
        msg["Bcc"] = bcc
    msg["Subject"] = subject
    msg.set_content(str(body))

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
            print(f"Attachment not found: {attachment_path}")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
            print(f"Email sent successfully to: {to}")
    except Exception as e:
        print(f"Failed to send to {to}: {e}")

for _, row in data.iterrows():
    send_email(
        to=row.get("To", ""),
        cc=row.get("CC", ""),
        bcc=row.get("BCC", ""),
        subject=row.get("Subject", ""),
        body=row.get("Body", ""),
        attachment=row.get("Attachment", "")
    )
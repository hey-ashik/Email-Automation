"""
Flask Email Automation Dashboard
Main application entry point - integrates existing email automation with modern web UI
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename
import pandas as pd
import requests
from io import StringIO

# Import our custom modules
from config_handler import load_config, save_config
from utils import (
    send_bulk_emails_async, 
    stop_sending, 
    get_sending_status, 
    get_email_logs, 
    clear_email_logs,
    validate_excel_columns,
    get_file_email_count
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main dashboard"""
    config = load_config()
    return render_template('index.html', config=config)

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    config = load_config()
    # Don't send password to frontend for security
    safe_config = {k: v for k, v in config.items() if k != 'sender_password'}
    safe_config['has_password'] = bool(config.get('sender_password'))
    return jsonify(safe_config)

@app.route('/api/config', methods=['POST'])
def update_config():
    """Update email configuration"""
    try:
        data = request.json
        config = load_config()
        
        # Update only provided fields
        if 'sender_email' in data:
            config['sender_email'] = data['sender_email']
        if 'sender_password' in data:
            config['sender_password'] = data['sender_password']
        if 'sender_name' in data:
            config['sender_name'] = data['sender_name']
        if 'smtp_server' in data:
            config['smtp_server'] = data['smtp_server']
        if 'smtp_port' in data:
            config['smtp_port'] = int(data['smtp_port'])
        
        save_config(config)
        
        return jsonify({
            'success': True,
            'message': 'Configuration updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating configuration: {str(e)}'
        }), 400

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload (Excel/CSV)"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            }), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Validate columns
            is_valid, missing, preview = validate_excel_columns(filepath)
            
            if not is_valid:
                return jsonify({
                    'success': False,
                    'message': f'Missing required columns: {", ".join(missing)}',
                    'missing_columns': missing
                }), 400
            
            # Get total email count
            total_count = get_file_email_count(filepath)
            
            return jsonify({
                'success': True,
                'message': 'File uploaded successfully',
                'filename': filename,
                'filepath': filepath,
                'preview': preview,
                'total_emails': total_count
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid file type. Please upload Excel (.xlsx, .xls) or CSV (.csv) file'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error uploading file: {str(e)}'
        }), 500

@app.route('/api/google-sheet', methods=['POST'])
def load_google_sheet():
    """Load data from Google Sheets public link"""
    try:
        data = request.json
        sheet_url = data.get('url', '')
        
        if not sheet_url:
            return jsonify({
                'success': False,
                'message': 'No Google Sheet URL provided'
            }), 400
        
        # Convert Google Sheets URL to CSV export URL
        if '/edit' in sheet_url:
            sheet_url = sheet_url.split('/edit')[0]
        
        csv_url = f"{sheet_url}/export?format=csv"
        
        # Download the sheet
        response = requests.get(csv_url)
        response.raise_for_status()
        
        # Save as CSV file
        filename = f"google_sheet_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        # Validate columns
        is_valid, missing, preview = validate_excel_columns(filepath)
        
        if not is_valid:
            return jsonify({
                'success': False,
                'message': f'Missing required columns: {", ".join(missing)}',
                'missing_columns': missing
            }), 400
        
        # Get total email count
        total_count = get_file_email_count(filepath)
        
        return jsonify({
            'success': True,
            'message': 'Google Sheet loaded successfully',
            'filename': filename,
            'filepath': filepath,
            'preview': preview,
            'total_emails': total_count
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading Google Sheet: {str(e)}'
        }), 500

@app.route('/api/send', methods=['POST'])
def send_emails():
    """Start sending emails"""
    try:
        data = request.json
        filepath = data.get('filepath', '')
        sender_name = data.get('sender_name', '')
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'message': 'No valid file to send emails from'
            }), 400
        
        # Check if already sending
        status = get_sending_status()
        if status['is_sending']:
            return jsonify({
                'success': False,
                'message': 'Email sending already in progress'
            }), 400
        
        # Start sending in background
        send_bulk_emails_async(filepath, sender_name)
        
        return jsonify({
            'success': True,
            'message': 'Email sending started'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error starting email send: {str(e)}'
        }), 500

@app.route('/api/stop', methods=['POST'])
def stop_emails():
    """Stop sending emails"""
    try:
        stop_sending()
        return jsonify({
            'success': True,
            'message': 'Email sending stopped'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error stopping emails: {str(e)}'
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current sending status"""
    status = get_sending_status()
    logs = get_email_logs()
    
    return jsonify({
        'is_sending': status['is_sending'],
        'should_stop': status['should_stop'],
        'total_emails': status['total_emails'],
        'sent_count': status['sent_count'],
        'failed_count': status['failed_count'],
        'total_logs': len(logs),
        'recent_logs': logs[-5:] if logs else []  # Last 5 logs
    })

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get all email logs"""
    logs = get_email_logs()
    return jsonify({
        'success': True,
        'logs': logs
    })

@app.route('/api/logs/clear', methods=['POST'])
def clear_logs():
    """Clear all email logs"""
    clear_email_logs()
    return jsonify({
        'success': True,
        'message': 'Logs cleared'
    })

if __name__ == '__main__':
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    print("=" * 60)
    print("🚀 Email Automation Dashboard Started")
    print("=" * 60)
    print("📧 Access the dashboard at: http://127.0.0.1:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

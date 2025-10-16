"""
Configuration Handler Module
Handles loading and saving of email configuration dynamically
"""
import json
import os

CONFIG_FILE = "config.json"

def load_config():
    """Load configuration from config.json file"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        # Return default configuration
        return {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "",
            "sender_password": "",
            "sender_name": ""
        }

def save_config(config_data):
    """Save configuration to config.json file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f, indent=4)
    return True

def update_config(key, value):
    """Update a single configuration value"""
    config = load_config()
    config[key] = value
    save_config(config)
    return config

def get_config_value(key):
    """Get a single configuration value"""
    config = load_config()
    return config.get(key, "")

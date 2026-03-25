#!/usr/bin/env python3
# hids_logging.py 

import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "your-email@gmail.com"
EMAIL_PASSWORD = "your-password"
EMAIL_RECIPIENT = "alerts@islandpay.com"

LOG_FILE = "hids.log"

def write_log(event_type, severity, source, description):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} | {event_type} | {severity} | {source} | {description}\n"
    
    try:
        with open(LOG_FILE, "a") as log_file:
            log_file.write(log_entry)
        print(f"[LOGGED] {log_entry.strip()}")
    except Exception as e:
        print(f"[ERROR] Failed to write to log file: {e}")

def send_email_alert(subject, message_body, severity="HIGH"):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECIPIENT
        msg['Subject'] = f"[{severity}] {subject}"
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        full_message = f"""
========================================
HIDS SECURITY ALERT
========================================

Time: {current_time}
Severity: {severity}

DETAILS:
{message_body}

========================================
This alert was generated automatically by
IslandPay Host-Based Intrusion Detection System
========================================
        """
        
        msg.attach(MIMEText(full_message, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        write_log("ALERT_SENT", "INFO", "EMAIL_SYSTEM", 
                 f"Alert sent: {subject} to {EMAIL_RECIPIENT}")
        
        print(f"[EMAIL] Alert sent successfully: {subject}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        error_msg = "Email authentication failed. Check email/password"
        print(f"[EMAIL ERROR] {error_msg}")
        write_log("ALERT_FAILED", "HIGH", "EMAIL_SYSTEM", error_msg)
        return False
        
    except smtplib.SMTPException as e:
        error_msg = f"SMTP error: {str(e)}"
        print(f"[EMAIL ERROR] {error_msg}")
        write_log("ALERT_FAILED", "HIGH", "EMAIL_SYSTEM", error_msg)
        return False
        
    except Exception as e:
        error_msg = f"Unexpected email error: {str(e)}"
        print(f"[EMAIL ERROR] {error_msg}")
        write_log("ALERT_FAILED", "HIGH", "EMAIL_SYSTEM", error_msg)
        return False

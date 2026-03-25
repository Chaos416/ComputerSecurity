#!/usr/bin/env python3

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
        
        print(f"[EMAIL] Alert sent successfully: {subject}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        error_msg = "Email authentication failed. Check email/password"
        print(f"[EMAIL ERROR] {error_msg}")
        return False
        
    except smtplib.SMTPException as e:
        error_msg = f"SMTP error: {str(e)}"
        print(f"[EMAIL ERROR] {error_msg}")
        return False
        
    except Exception as e:
        error_msg = f"Unexpected email error: {str(e)}"
        print(f"[EMAIL ERROR] {error_msg}")
        return False

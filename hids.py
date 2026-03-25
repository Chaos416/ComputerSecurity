#!/usr/bin/env python3
"""
Main HIDS Control Script 
"""

import os
from datetime import datetime
from file_integrity import build_baseline, check_file_integrity
from ssh_detection import check_ssh_bruteforce
from logging_alerting import write_log, send_email_alert

def main():
    print("=" * 60)
    print("IslandPay HIDS - Host-Based Intrusion Detection System")
    print(f"Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    BASELINE_FILE = "baseline.json"
    
    if not os.path.exists(BASELINE_FILE):
        print("[WARNING] No baseline found. Creating baseline first...")
        build_baseline()
        print()
    
    print("\n[1/2] Running File Integrity Check...")
    check_file_integrity()
    
    print("\n[2/2] Running SSH Brute Force Detection...")
    check_ssh_bruteforce()
    
    print("\n" + "=" * 60)
    print(f"Scan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Check hids.log for detailed logs")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Scan interrupted by user")
        write_log("SYSTEM", "INFO", "SYSTEM", "HIDS scan interrupted by user")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        write_log("SYSTEM", "HIGH", "SYSTEM", f"Unexpected error: {str(e)}")

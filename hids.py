#!/usr/bin/env python3
"""
Main HIDS Control Script 
IslandPay Tech Ltd. - Host-Based Intrusion Detection System
"""

import os
import sys
from datetime import datetime

# Import group members' logging and alerting module (Requirements C & D)
from hids_logging import write_log, send_email_alert

# Import group member's file integrity module (Requirement A)
from file_integrity import scan_directory, load_baseline, save_baseline, compare_files

# Import group member's SSH detection module (Requirement B)
from ssh_detection import check_ssh_bruteforce

# Configuration
MONITOR_DIR = "/etc"  
BASELINE_FILE = "baseline.json"

def run_file_integrity():
    """Run file integrity monitoring and handle logging/alerting"""
    
    print("\n[1/2] Running File Integrity Check...")
    print("-" * 40)
    
    write_log("INTEGRITY_CHECK_START", "INFO", "SYSTEM", 
              f"Starting file integrity scan on {MONITOR_DIR}")
    
    # Scan current directory
    print("Scanning directory...")
    current_scan = scan_directory(MONITOR_DIR)
    baseline = load_baseline(BASELINE_FILE)
    
    # First run: create baseline
    if not baseline:
        print("No baseline found. Creating baseline...")
        save_baseline(current_scan, BASELINE_FILE)
        print(f"Baseline saved successfully with {len(current_scan)} files.")
        write_log("BASELINE_CREATED", "INFO", "SYSTEM", 
                  f"Baseline created for {MONITOR_DIR} with {len(current_scan)} files")
        return
    
    # Compare files
    modified, new, deleted = compare_files(current_scan, baseline)
    
    # Process modified files
    for file_path in modified:
        print(f"  [MODIFIED] {file_path}")
        write_log("FILE_MODIFIED", "MEDIUM", file_path, "File content changed")
        send_email_alert("File Modified", 
                        f"File: {file_path}\nAction: Modified\nDirectory: {MONITOR_DIR}", 
                        "MEDIUM")
    
    # Process new files
    for file_path in new:
        print(f"  [NEW] {file_path}")
        write_log("FILE_NEW", "MEDIUM", file_path, "New file detected")
        send_email_alert("New File Detected", 
                        f"File: {file_path}\nAction: Added\nDirectory: {MONITOR_DIR}", 
                        "MEDIUM")
    
    # Process deleted files
    for file_path in deleted:
        print(f"  [DELETED] {file_path}")
        write_log("FILE_DELETED", "HIGH", file_path, "File missing from system")
        send_email_alert("File Deleted", 
                        f"File: {file_path}\nAction: Deleted\nDirectory: {MONITOR_DIR}", 
                        "HIGH")
    
    # Print summary
    print(f"\nFile Integrity Summary:")
    print(f"  Modified: {len(modified)}")
    print(f"  New: {len(new)}")
    print(f"  Deleted: {len(deleted)}")
    
    write_log("INTEGRITY_CHECK_COMPLETE", "INFO", "SYSTEM", 
              f"Scan complete: {len(modified)} modified, {len(new)} new, {len(deleted)} deleted")

def run_ssh_check():
    """Run SSH brute force detection"""
    
    print("\n[2/2] Running SSH Brute Force Detection...")
    print("-" * 40)
    
    # The function should handle its own logging and alerts
    check_ssh_bruteforce()

def main():
    """Main control script"""
    
    print("=" * 60)
    print("IslandPay HIDS - Host-Based Intrusion Detection System")
    print(f"Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check if running as root
    if os.geteuid() != 0:
        print("\n[WARNING] Not running as root.")
        print("         Some files in /etc may not be accessible.")
        print("         Run with sudo for full functionality.\n")
        write_log("PERMISSION_WARNING", "MEDIUM", "SYSTEM", 
                 "Not running as root - some files may be inaccessible")
    
    # Run file integrity check (Requirement A)
    run_file_integrity()
    
    # Run SSH brute force detection (Requirement B)
    run_ssh_check()
    
    # Final summary
    print("\n" + "=" * 60)
    print(f"Scan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Log file: hids.log")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Scan interrupted by user")
        write_log("SYSTEM_INTERRUPT", "INFO", "SYSTEM", "HIDS scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        write_log("SYSTEM_ERROR", "HIGH", "SYSTEM", f"Unexpected error: {str(e)}")
        sys.exit(1)

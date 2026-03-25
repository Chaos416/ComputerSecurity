import os
import hashlib
import json

# Generate SHA-256 hash of a file
def hash_file(file_path):
    try:
        with open(file_path, "rb") as f:
            content = f.read()
            return hashlib.sha256(content).hexdigest()
    except:
        return None

# Scan directory and hash all files
def scan_directory(directory):
    file_hashes = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            file_hash = hash_file(path)

            if file_hash:
                file_hashes[path] = file_hash

    return file_hashes

# Save baseline to JSON file
def save_baseline(data, filename="baseline.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Load baseline from JSON file
def load_baseline(filename="baseline.json"):
    if not os.path.exists(filename):
        return {}

    with open(filename, "r") as f:
        return json.load(f)

# Compare current scan with baseline
def compare_files(current, baseline):
    modified = []
    new = []
    deleted = []

    # Check new and modified files
    for file in current:
        if file not in baseline:
            new.append(file)
        elif current[file] != baseline[file]:
            modified.append(file)

    # Check deleted files
    for file in baseline:
        if file not in current:
            deleted.append(file)

    return modified, new, deleted

# Main function for standalone testing
def main():
    directory = "test_folder"

    print("Scanning directory...")
    current_scan = scan_directory(directory)

    baseline = load_baseline()

    # First run: create baseline
    if not baseline:
        print("No baseline found. Creating baseline...")
        save_baseline(current_scan)
        print("Baseline saved successfully.")
        print("Run the script again to detect changes.")

    # Second run: compare
    else:
        print("\n--- FILE CHANGE RESULTS ---")

        modified, new, deleted = compare_files(current_scan, baseline)

        print(f"Modified files ({len(modified)}): {modified}")
        print(f"New files ({len(new)}): {new}")
        print(f"Deleted files ({len(deleted)}): {deleted}")

# Run program
if __name__ == "__main__":
    main()

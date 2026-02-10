# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
import os
import re

def check_headers(directory):
    files_missing_headers = []
    # common header patterns
    header_patterns = [
        r"copyright",
        r"credit to the owner",
        r"protected by",
        r"author:"
    ]
    regex = re.compile("|".join(header_patterns), re.IGNORECASE)

    for root, dirs, files in os.walk(directory):
        # Skip some directories
        if any(skip in root for skip in [".git", "__pycache__", ".venv", ".antigravity"]):
            continue
            
        for file in files:
            if file.endswith((".py", ".sh", ".pyz")):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        # Check first 20 lines
                        head = "".join([f.readline() for _ in range(20)])
                        if not regex.search(head):
                            files_missing_headers.append(path)
                except Exception:
                    pass
    
    return files_missing_headers

if __name__ == "__main__":
    missing = check_headers("/home/son/CLAWBOLT")
    if missing:
        print(f"⚠️ Found {len(missing)} files missing copyright/credit headers:")
        for f in missing:
            print(f"- {f}")
    else:
        print("✅ All checked files have credit/copyright headers!")

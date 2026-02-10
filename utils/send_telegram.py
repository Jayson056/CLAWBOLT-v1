# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
#!/usr/bin/env python3
import sys
import requests
import os
import time

# Configuration (Mirrored from telegram_bridge.py)
BOT_TOKEN = "7961814507:AAH8d2r4erdsEtGl88U99Q9HehFixQ4tBlo"
AUTHORIZED_CHAT_ID = 5662168844
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

def send_message(text, parse_mode="Markdown", retries=3):
    if not text:
        print("Error: No message text provided.")
        return False
        
    # Auto-add emojis/theme based on content keywords if not already present
    if "✅" not in text and "❌" not in text and "ℹ️" not in text:
        if "success" in text.lower() or "done" in text.lower():
            text = f"✅ *SUCCESS*\n\n{text}"
        elif "error" in text.lower() or "fail" in text.lower():
            text = f"❌ *ERROR*\n\n{text}"
        elif "warning" in text.lower():
            text = f"⚠️ *WARNING*\n\n{text}"
        else:
            text = f"ℹ️ *UPDATE*\n\n{text}"

    for attempt in range(retries):
        try:
            response = requests.post(API_URL + "sendMessage", json={
                "chat_id": AUTHORIZED_CHAT_ID,
                "text": text,
                "parse_mode": parse_mode
            }, timeout=10)
            
            if response.status_code == 200:
                print("Message sent successfully.")
                return True
            else:
                print(f"Attempt {attempt+1} failed: {response.text}")
        except Exception as e:
            print(f"Attempt {attempt+1} error: {e}")
        
        if attempt < retries - 1:
            time.sleep(2)
            
    print("Failed to send message after all retries.")
    return False

def send_document(file_path, retries=3):
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return False
    
    for attempt in range(retries):
        try:
            with open(file_path, "rb") as doc:
                response = requests.post(API_URL + "sendDocument", data={
                    "chat_id": AUTHORIZED_CHAT_ID
                }, files={
                    "document": doc
                }, timeout=300)
                
                if response.status_code == 200:
                    print(f"File '{os.path.basename(file_path)}' sent successfully.")
                    return True
                else:
                    print(f"Attempt {attempt+1} failed: {response.text}")
        except Exception as e:
            print(f"Attempt {attempt+1} error: {e}")
        
        if attempt < retries - 1:
            time.sleep(2)
            
    print("Failed to send document after all retries.")
    return False

def send_voice(file_path, retries=3):
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return False
    
    for attempt in range(retries):
        try:
            with open(file_path, "rb") as voice:
                response = requests.post(API_URL + "sendVoice", data={
                    "chat_id": AUTHORIZED_CHAT_ID
                }, files={
                    "voice": voice
                }, timeout=300)
                
                if response.status_code == 200:
                    print(f"Voice message sent successfully.")
                    return True
                else:
                    print(f"Attempt {attempt+1} failed: {response.text}")
        except Exception as e:
            print(f"Attempt {attempt+1} error: {e}")
            
        if attempt < retries - 1:
            time.sleep(2)
            
    print("Failed to send voice after all retries.")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 send_telegram.py 'Message text'")
        print("  python3 send_telegram.py --file /path/to/file")
        print("  python3 send_telegram.py --voice /path/to/voice.mp3")
        sys.exit(1)
    
    if sys.argv[1] in ["--file", "-f"] and len(sys.argv) >= 3:
        file_path = sys.argv[2]
        success = send_document(file_path)
    elif sys.argv[1] in ["--voice", "-v"] and len(sys.argv) >= 3:
        file_path = sys.argv[2]
        success = send_voice(file_path)
    else:
        message = " ".join(sys.argv[1:])
        success = send_message(message)
    
    sys.exit(0 if success else 1)

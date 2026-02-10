# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
import sys
import os
import time
from gtts import gTTS

def text_to_mp3(text, output_file=None, retries=3):
    """Converts text to speech and saves as MP3 with timestamp support."""
    # Create storage directory if it doesn't exist
    storage_dir = "/home/son/CLAWBOLT/storage"
    os.makedirs(storage_dir, exist_ok=True)
    
    if not output_file:
        timestamp = int(time.time())
        output_file = os.path.join(storage_dir, f"speech_{timestamp}.mp3")
    
    # Ensure path is absolute for clarity
    abs_output = os.path.abspath(output_file)
    
    # Clean text for TTS
    clean_text = text.replace("*", "").replace("_", "").replace("`", "")
    
    for attempt in range(retries):
        try:
            tts = gTTS(text=clean_text, lang='en')
            tts.save(abs_output)
            return True, abs_output
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
                continue
            return False, str(e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 text_to_speech.py \"Text to speak\" [output_file]")
        sys.exit(1)
        
    text = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    success, result = text_to_mp3(text, output)
    if success:
        # Print the absolute path as the ONLY output line for easy capture by other scripts
        print(result)
        sys.exit(0)
    else:
        print(f"❌ Error: {result}")
        sys.exit(1)

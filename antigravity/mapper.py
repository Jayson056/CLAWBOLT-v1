# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
import logging
import pytesseract
import cv2
import numpy as np
import os
import json

logger = logging.getLogger(__name__)

CACHE_FILE = "/home/son/CLAWBOLT/storage/mapper_cache.json"
KEYWORDS = ["ask anything (Ctrl+L)","@ to mention" "/ for workflows", "(ctrl+l)"]
OFFSET_Y = 10  # Pixels within/near the label to click

def locate_input_box():
    """
    Capture screen, run OCR, and find the input box coordinates.
    Returns (x, y) tuple or None.
    """
    try:
        # Lazy import to support headless backend
        import pyautogui
        
        # Capture full screen
        screenshot = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Run OCR
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

        screen_width, screen_height = screenshot.size
        half_width = screen_width // 2
        
        matches = []
        for i, text in enumerate(data["text"]):
            text_clean = text.lower().strip()
            if not text_clean:
                continue
            
            # Context words for phrase matching (wider window)
            context_window = 6
            context_words = data["text"][max(0, i-2):i+context_window]
            context_phrase = " ".join([w.lower().strip() for w in context_words if w.strip()]).strip()
            
            match_found = False
            # OCR can be flaky, search for combinations
            if "ask" in text_clean and ("any" in context_phrase or "thing" in context_phrase):
                match_found = True
            elif "type" in text_clean and "your" in context_phrase:
                match_found = True
            elif "mention" in context_phrase or "workflows" in context_phrase:
                match_found = True
            elif "ctrl" in text_clean or "+l" in context_phrase:
                match_found = True
            elif "anything" in text_clean:
                match_found = True

            if match_found:
                x = data["left"][i]
                y = data["top"][i]
                width = data["width"][i]
                height = data["height"][i]
                
                # Center the click
                input_x = x + width // 2
                input_y = y + height // 2
                
                # CRITICAL: Ignore anything in the central Editor Zone (25% to 75% width)
                if (screen_width * 0.25) < input_x < (screen_width * 0.75):
                    continue

                # Higher priority for right side matches (Sidebar location)
                score = 0
                if input_x > screen_width * 0.7:
                    score += 5000  # Multiplier for sidebar priority
                
                # Boost based on vertical position (it's usually near the bottom)
                if input_y > screen_height * 0.7:
                    score += 500
                
                # Bonus for full phrase matches
                if "ask anything" in context_phrase:
                    score += 300
                if "(ctrl+l)" in context_phrase or "ctrl+l" in context_phrase:
                    score += 400

                matches.append({
                    "coords": (input_x, input_y),
                    "phrase": context_phrase,
                    "score": score
                })

        if matches:
            # Pick the best match (highest score)
            best_match = max(matches, key=lambda m: m["score"])
            logger.info(f"Input box found at {best_match['coords']} (score: {best_match['score']})")
            
            # Save to cache
            try:
                os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
                with open(CACHE_FILE, 'w') as f:
                    json.dump({"last_x": int(best_match['coords'][0]), "last_y": int(best_match['coords'][1])}, f)
            except Exception as e:
                logger.warning(f"Failed to cache location: {e}")
                
            return best_match["coords"]

        # Fallback 1: Try Cache
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, 'r') as f:
                    cache = json.load(f)
                    logger.info(f"Using cached input box location: ({cache['last_x']}, {cache['last_y']})")
                    return (cache['last_x'], cache['last_y'])
            except:
                pass

        # Fallback 2: Hard-coded Sidebar location
        logger.warning("Input box keywords not found via OCR. Using layout fallback.")
        sidebar_x = screen_width - (screen_width // 6) # Far right
        sidebar_y = screen_height - 100
        return (sidebar_x, sidebar_y)

    except Exception as e:
        logger.error(f"OCR mapping failed: {e}")
        return None
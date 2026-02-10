# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
import logging
import pytesseract
import cv2
import numpy as np

logger = logging.getLogger(__name__)

# Keywords to identify action buttons
ACCEPT_KEYWORDS = ["accept", "apply", "confirm", "allow once", "allow this conversation"]
REJECT_KEYWORDS = ["reject", "dismiss", "cancel", "discard", "deny"]
ALL_KEYWORD = "all"
ALLOW_KEYWORDS = ["allow", "access"]

def detect_action_buttons():
    """
    Scan the screen for Accept ALL and Reject ALL buttons using phrase detection.
    
    Returns:
        dict or None: {"accept_all": (x, y), "reject_all": (x, y)} if found, else None
    """
    try:
        # Lazy import to support headless backend
        import pyautogui
        
        # Capture full screen
        screenshot = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Run OCR with detailed output
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        
        screen_width, screen_height = screenshot.size
        # The sidebar is usually on the right
        
        detected = {}
        
        # We search for sequences like "Accept" + "all" on the same line
        for i, text in enumerate(data["text"]):
            text_clean = text.lower().strip()
            if not text_clean:
                continue
            
            y = data["top"][i]
            x = data["left"][i]
            
            # Context window - look for a phrase on the same line
            context_parts = []
            for j in range(max(0, i-2), min(len(data["text"]), i+3)):
                if abs(data["top"][j] - y) < 15:
                    context_parts.append(data["text"][j].strip().lower())
            
            full_phrase = " ".join(context_parts)
            
            # Targeted phrase detection with strict ordering for the blue button and label
            is_accept_all = "accept all" in full_phrase or "apply all" in full_phrase
            is_reject_all = "reject all" in full_phrase or "dismiss all" in full_phrase or "discard all" in full_phrase
            is_allow_once = "allow once" in full_phrase
            is_allow_conv = "allow this conversation" in full_phrase or "allow conversion" in full_phrase

            button_x = x + data["width"][i] // 2
            button_y = y + data["height"][i] // 2
            
            # Context-aware mapping
            if is_accept_all and text_clean in ["accept", "apply"]:
                detected["accept_all"] = (button_x, button_y)
            
            if is_reject_all and text_clean in ["reject", "dismiss", "discard"]:
                detected["reject_all"] = (button_x, button_y)

            if is_allow_once and text_clean in ["allow", "once"]:
                detected["allow_once"] = (button_x, button_y)

            if is_allow_conv and text_clean in ["allow", "this", "conversation"]:
                detected["allow_conv"] = (button_x, button_y)

        if detected:
            return detected
        
        # Fallback 2: Try looking for just keywords if phrase matching failed
        logger.warning("No phrase-based Accept/Reject buttons detected, trying keyword fallback...")
        for i, text in enumerate(data["text"]):
            text_clean = text.lower().strip()
            if text_clean in ["accept", "reject"] and data["left"][i] > screen_width * 0.6:
                 key = f"{text_clean}_all"
                 if key not in detected:
                     detected[key] = (data["left"][i] + data["width"][i]//2, data["top"][i] + data["height"][i]//2)
        
        return detected if detected else None
        
    except Exception as e:
        logger.error(f"Button detection failed: {e}")
        return None


def click_button(coords):
    """
    Click at the specified coordinates.
    
    Args:
        coords (tuple): (x, y) coordinates to click
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Lazy import to support headless backend
        import pyautogui
        import time
        
        x, y = coords
        logger.info(f"Clicking button at ({x}, {y})")
        
        # Move to position
        pyautogui.moveTo(x, y, duration=0.2)
        time.sleep(0.1)
        
        # Click
        pyautogui.click(x, y)
        logger.info(f"Successfully clicked at ({x}, {y})")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to click button at {coords}: {e}")
        return False

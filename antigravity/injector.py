# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
import time
import logging
from antigravity.window import focus_antigravity
from antigravity.mapper import locate_input_box

logger = logging.getLogger(__name__)

from antigravity.skill_manager import get_skill_header

def get_context():
    return get_skill_header()

def send_to_antigravity(user_text):
    """
    Focus window, find input box, and inject text.
    Returns (success, message).
    """
    if not focus_antigravity():
        return False, "Antigravity window not found"

    # Wait for window to settle/render
    time.sleep(0.5)

    location = None
    for attempt in range(3):
        location = locate_input_box()
        if location:
            break
        logger.warning(f"Input box not found (attempt {attempt+1}/3). Retrying...")
        time.sleep(1.0)

    if not location:
        return False, "Input box not detected after retries"

    x, y = location
    try:
        # Lazy import to support headless backend
        import pyautogui
        import pyperclip
        
        pyautogui.click(x, y)
        time.sleep(0.2)
        
        # Inject context + user text + reinforcement footer
        footer = "\n\n(IMPORTANT: Send your response via Telegram using the provided script)"
        full_text = f"{get_context()}\n\n{user_text}{footer}"
        
        # Use clipboard for reliable, instant pasting
        pyperclip.copy(full_text)
        
        # Select all (Ctrl+A) and paste (Ctrl+V) to replace existing content cleanly
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        
        pyautogui.press("enter")
        
        return True, "Message sent to Antigravity"
    except Exception as e:
        logger.error(f"Injection failed: {e}")
        return False, f"Injection error: {e}"
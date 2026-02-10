# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
import logging
import os
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from telegram_interface.auth import is_authorized
from antigravity.injector import send_to_antigravity
from antigravity.monitor import detect_state, get_error_details
from telegram_interface.ui import accept_reject_keyboard

logger = logging.getLogger(__name__)

SCREENSHOTS_DIR = "storage/screenshots"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Route text messages to the appropriate handler."""
    user = update.effective_user
    if not user or not is_authorized(user.id):
        return

    message_text = update.message.text
    logger.info(f"Received message from {user.first_name}: {message_text}")
    
    # 1. Bot Detection: Check if busy before sending
    state = detect_state()
    if state == "busy":
        await update.message.reply_text("⚠️ **WAIT!** I'm still processing your previous request. Please wait for the response to finish. ⏳")
        return

    # 2. Attempt to send to Antigravity
    await update.message.reply_text("⏳ **Sending to Antigravity...**")
    success, status = send_to_antigravity(message_text)
    
    if success:
        # After sending, wait a moment and check if it immediately hit a limit
        await asyncio.sleep(1.0) # Brief pause for UI to update
        
        new_state = detect_state()
        if new_state == "error":
            error_msg = get_error_details()
            await update.message.reply_text(f"❌ **LIMIT REACHED**\n\n{error_msg}\n\nPlease check your quota or wait for the limit to reset.")
        else:
            # Success - wait for AI to finish and check for action buttons
            await wait_and_detect_buttons(update, context)
    else:
        await update.message.reply_text(f"❌ **Injection Failed**\n\n{status}")
        
        # Capture debug screenshot
        try:
            if not os.path.exists(SCREENSHOTS_DIR):
                os.makedirs(SCREENSHOTS_DIR)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{SCREENSHOTS_DIR}/error_{timestamp}.png"
            
            import pyautogui
            pyautogui.screenshot().save(filename)
            await update.message.reply_photo(photo=open(filename, 'rb'), caption="Debug View")
        except Exception as e:
            logger.error(f"Failed to send debug screenshot: {e}")

async def wait_and_detect_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Wait for AI to finish processing, then detect and send Accept/Reject buttons if available.
    """
    from antigravity.button_mapper import detect_action_buttons
    
    # Context-aware: If the message looks like a code edit, be more persistent
    message_text = update.message.text.lower() if update.message and update.message.text else ""
    is_code_edit = any(kw in message_text for kw in ["edit", "code", "change", "add", "remove", "update", "fix", "implement", "refactor"])
    
    # Wait for AI to finish (max 90 seconds for large edits)
    max_wait = 90
    waited = 0
    detected = False
    
    logger.info(f"Monitoring for buttons. Is code edit: {is_code_edit}")
    
    while waited < max_wait:
        state = detect_state()
        
        # Check for buttons even while busy, as they might appear before the state flips to idle
        try:
            buttons = detect_action_buttons()
            if buttons:
                # Send Accept/Reject buttons to Telegram
                await update.message.reply_text(
                    "🔧 **AI has made changes to files.**\n\nChoose an action:",
                    reply_markup=accept_reject_keyboard()
                )
                logger.info(f"Sent Accept/Reject buttons to user. Detected: {buttons}")
                detected = True
                break
        except Exception as e:
            logger.error(f"Button detection inside loop failed: {e}")

        if state == "idle" and waited > 5: # Give it at least 5s to actually start
            # AI finished, let's do one last thorough check
            await asyncio.sleep(2)
            buttons = detect_action_buttons()
            if buttons:
                await update.message.reply_text(
                    "🔧 **AI has made changes to files.**\n\nChoose an action:",
                    reply_markup=accept_reject_keyboard()
                )
                detected = True
            break
        elif state == "error":
            return
        
        await asyncio.sleep(3)
        waited += 3
    
    if not detected and is_code_edit:
        # If we expected a code edit but didn't see buttons, maybe OCR missed them
        # Offer buttons anyway as a fallback if the user might need them
        logger.warning("Code edit expected but no buttons detected. Offering fallback.")
        await update.message.reply_text(
            "📝 I didn't verify the file changes visually, but if I made edits, you can use these buttons to manage them:",
            reply_markup=accept_reject_keyboard()
        )
    elif not detected:
        logger.debug("No Accept/Reject buttons detected in Antigravity UI")


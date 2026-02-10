# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
import logging
import os
from telegram import Bot

logger = logging.getLogger(__name__)

async def send_startup_notification():
    """Send startup notification to user via Telegram."""
    from dotenv import load_dotenv
    load_dotenv(dotenv_path="config/secrets.env")
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    user_id = os.getenv("TELEGRAM_USER_ID")
    
    if not token or not user_id:
        logger.warning("Cannot send startup notification: missing token or user ID")
        return
    
    try:
        bot = Bot(token)
        message = """
🦅 **CLAWBOLT ONLINE**

System Status:
✅ Bot service started
✅ Antigravity launched
✅ Ready for commands

Type /rules to see available commands.
"""
        await bot.send_message(chat_id=user_id, text=message)
        logger.info("Startup notification sent")
    except Exception as e:
        logger.error(f"Failed to send startup notification: {e}")

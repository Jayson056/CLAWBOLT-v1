# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
import subprocess
import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram_interface.auth import is_authorized
from security.confirm import request_confirmation
from security.sudo_flow import set_awaiting_sudo, execute_with_sudo

logger = logging.getLogger(__name__)

async def sysrest_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Request system restart."""
    user = update.effective_user
    if not user or not is_authorized(user.id):
        return

    text, markup = request_confirmation(user.id, "SYSTEM_RESTART")
    await update.message.reply_markdown(text, reply_markup=markup)

async def execute_system_restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Executes the restart."""
    # Handle both callback query (from buttons) and regular message
    if update.callback_query:
        message = update.callback_query.message
    else:
        message = update.message
    
    await message.reply_text("🔄 Attempting to reboot system...")
    
    # Try without password first
    try:
        result = subprocess.run(["sudo", "-n", "reboot"], capture_output=True, timeout=2)
        if result.returncode == 0:
            # Success! (system will reboot)
            return
    except:
        pass  # Will handle below
    
    # Failed - needs password
    user = update.effective_user
    set_awaiting_sudo("SYSTEM_RESTART")
    await message.reply_text("🔐 **Sudo password required**\n\nPlease send your sudo password to execute the reboot.")

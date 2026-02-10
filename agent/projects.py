# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
import os
import subprocess
import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram_interface.auth import is_authorized

logger = logging.getLogger(__name__)

async def projects_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Open and list the workplace 'Projects' folder.
    Usage: /projects
    """
    user = update.effective_user
    if not user or not is_authorized(user.id):
        return

    # Path to projects folder (relative to repo root)
    # Using absolute path to be sure
    base_dir = "/home/son/CLAWBOLT_Workspaces/CLAWBOLT-v1"
    projects_path = os.path.join(base_dir, "Projects")

    if not os.path.exists(projects_path):
        try:
            os.makedirs(projects_path, exist_ok=True)
            logger.info(f"Created missing Projects directory at {projects_path}")
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to access Projects directory: {e}")
            return

    try:
        # 1. Attempt to open in file manager (GUI feedback for human)
        # Using xdg-open for cross-desktop compatibility
        subprocess.Popen(["xdg-open", projects_path], start_new_session=True)
        
        # 2. List contents for Telegram
        files = os.listdir(projects_path)
        files.sort()
        
        if not files:
            await update.message.reply_text("📂 **Projects Folder Opened**\n\nThe folder is currently empty.")
            return

        display_files = files[:50]
        output = "\n".join([f"📁 {f}" if os.path.isdir(os.path.join(projects_path, f)) else f"📄 {f}" for f in display_files])
        
        if len(files) > 50:
            output += f"\n\n... and {len(files) - 50} more items."

        await update.message.reply_text(f"📂 **Projects Folder Opened**\n\n**Location:** `{projects_path}`\n\n**Contents:**\n{output}")
        
    except Exception as e:
        logger.error(f"Error opening projects: {e}")
        await update.message.reply_text(f"❌ Error opening Projects: {e}")

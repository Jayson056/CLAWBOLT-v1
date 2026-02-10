# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
import logging
from telegram import Update
from telegram.ext import ContextTypes

# Import command handlers
from agent.rules import rules_command
from agent.screen import screen_command
from agent.report import report_command
from agent.restart import restart_antigravity
from agent.ls import list_dir
from agent.watch import watch_command
from agent.hear import hear_command
from agent.sysrest import sysrest_command
from agent.syslogout import syslogout_command
from agent.quota import show_quota
from agent.save import save_snapshot
from agent.passkey import pass_command
from agent.select_model import select_model_command
from agent.select_skill import select_skill_command
from agent.actions import accept_command, reject_command
from agent.projects import projects_command
from telegram_interface.auth import is_authorized # Needed for start check

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message."""
    user = update.effective_user
    if not user or not is_authorized(user.id):
        return
    await update.message.reply_text(f"⚡ CLAWBOLT Active!\nWelcome, {user.first_name}.\nUse /rules to see commands.")

# Command Descriptions for Telegram Menu
COMMAND_DESCRIPTIONS = {
    "start": "Verify CLAWBOLT connectivity",
    "rules": "Show all available commands",
    "help": "Show all available commands",
    "screen": "Capture and send current desktop screenshot",
    "report": "Get system status report (CPU, RAM, Disk)",
    "restart": "Restart the Antigravity AI interface",
    "ls": "List directory contents (usage: /ls [path])",
    "watch": "Monitor screen for changes",
    "hear": "Listen to the last 10s of system audio",
    "sysrest": "Restart the entire system (OS)",
    "syslogout": "Log out the current desktop session",
    "quota": "Check AI model usage limits",
    "save": "Save a conversation snapshot",
    "pass": "Send password for keyring (usage: /pass [pwd])",
    "select_model": "Open interactive model selection menu",
    "select_skill": "Switch AI persona/skills mode",
    "accept": "Click 'Accept ALL' in Antigravity UI",
    "reject": "Click 'Reject ALL' in Antigravity UI",
    "projects": "Open and list the workplace projects folder",
}

# Command Registry
COMMANDS = {
    "/start": start_command, # Ensure explicit start handling
    "/rules": rules_command,
    "/help": rules_command,
    "/screen": screen_command,
    "/report": report_command,
    "/restart": restart_antigravity,
    "/ls": list_dir,
    "/watch": watch_command,
    "/hear": hear_command,
    "/sysrest": sysrest_command,
    "/syslogout": syslogout_command,
    "/quota": show_quota,
    "/save": save_snapshot,
    "/pass": pass_command,
    "/select_model": select_model_command,
    "/select_skill": select_skill_command,
    "/accept": accept_command,
    "/reject": reject_command,
    "/projects": projects_command,
}

async def route_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Route a command to its appropriate handler.
    Expected update.message.text to start with /.
    """
    text = update.message.text
    if not text:
        return

    # Extract command (first word) and handle @botname
    full_cmd = text.split()[0].lower()
    cmd = full_cmd.split('@')[0]
    
    # Check if command exists in registry
    handler = COMMANDS.get(cmd)
    
    if handler:
        logger.info(f"Routing command: {cmd}")
        try:
            await handler(update, context)
        except Exception as e:
            logger.error(f"Error in handler for {cmd}: {e}")
            await update.message.reply_text(f"❌ Error executing command: {e}")
    else:
        # Avoid replying to unknown commands in groups if they aren't for us
        if '@' in full_cmd and not full_cmd.endswith(context.bot.username.lower()):
            return
            
        await update.message.reply_text("❌ Unknown command. Use /rules to see available commands.")


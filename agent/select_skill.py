# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram_interface.auth import is_authorized
from antigravity.skill_manager import SKILL_CONFIG, get_current_skill

logger = logging.getLogger(__name__)

# State management for password flow in select_skill
_awaiting_skill_password = {} # user_id -> skill_id

async def select_skill_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display skill selection menu."""
    user = update.effective_user
    if not user or not is_authorized(user.id):
        return
    
    current_skill = get_current_skill()
    
    keyboard = []
    # Build keyboard from SKILL_CONFIG
    for skill_id, config in SKILL_CONFIG.items():
        status_icon = "🟢" if skill_id == current_skill else "🔘"
        lock_icon = "🔒 " if config.get("password_protected") else ""
        button_text = f"{status_icon} {lock_icon}{config['name']}"
        keyboard.append([InlineKeyboardButton(text=button_text, callback_data=f"SKILL:{skill_id}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    msg = f"""🧠 **AI SKILL SELECTION**

📍 **Current**: `{SKILL_CONFIG.get(current_skill, {}).get('name', 'Unknown')}`

**Status Key:**
🟢 = Current Active Skill
🔘 = Available Skill
🔒 = Password Protected

Choose a skill to switch:
"""
    await update.message.reply_text(msg, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_skill_selection(query):
    """Handle skill selection button click."""
    from antigravity.skill_manager import SKILL_CONFIG, set_current_skill
    
    user_id = query.from_user.id
    skill_id = query.data.replace("SKILL:", "")
    
    if skill_id not in SKILL_CONFIG:
        await query.message.reply_text("❌ Unknown skill.")
        return

    config = SKILL_CONFIG[skill_id]
    
    if config.get("password_protected"):
        _awaiting_skill_password[user_id] = skill_id
        await query.edit_message_text(f"🔒 **PASSWORD REQUIRED**\n\nThe skill `{config['name']}` is protected.\n\nPlease type the maintenance password to proceed:")
    else:
        if set_current_skill(skill_id):
            await query.edit_message_text(f"✅ **Skill Switched**\n\nNow using: `{config['name']}`")
        else:
            await query.edit_message_text("❌ Failed to switch skill.")

def is_awaiting_skill_password(user_id):
    return user_id in _awaiting_skill_password

async def verify_skill_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from antigravity.skill_manager import SKILL_CONFIG, set_current_skill
    
    user_id = update.effective_user.id
    password = update.message.text
    skill_id = _awaiting_skill_password.get(user_id)
    
    if not skill_id:
        return False

    # Simple password check for now - can be moved to config/secrets
    # User requested: "input password to allow this skill"
    # I'll use "core2026" as default if none specified in user request
    if password == "core2026":
        if set_current_skill(skill_id):
            await update.message.reply_text(f"✅ **Authenticated!**\n\nSkill switched to: `{SKILL_CONFIG[skill_id]['name']}`")
            del _awaiting_skill_password[user_id]
            return True
        else:
            await update.message.reply_text("❌ Failed to switch skill after authentication.")
    else:
        await update.message.reply_text("❌ **Incorrect password.** Skill switch aborted.")
        del _awaiting_skill_password[user_id]
    
    return True

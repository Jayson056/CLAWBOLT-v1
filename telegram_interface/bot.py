# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram_interface.auth import is_authorized

from agent.screen import screen_command
from agent.report import report_command
from core.router import handle_message

# Load environment variables
from dotenv import load_dotenv
load_dotenv(dotenv_path="config/secrets.env")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# ... imports ...
from telegram.ext import CallbackQueryHandler
from security.confirm import resolve_confirmation
from agent.router import route_command, COMMANDS, COMMAND_DESCRIPTIONS
from security.password_flow import is_awaiting_password, set_password, inject_password, set_awaiting_password
from security.detector import detect_password_prompt
from security.sudo_flow import is_awaiting_sudo, get_pending_sudo_action, set_sudo_password, execute_with_sudo
from core.router import handle_message as core_handle_message
from agent.sysrest import execute_system_restart
from agent.syslogout import execute_system_logout
from agent.select_skill import is_awaiting_skill_password, verify_skill_password, handle_skill_selection
from telegram import BotCommand

# Wrapper to intercept messages for password flow only (confirmation handled by buttons now)
async def handle_message_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or not is_authorized(user.id):
        return

    text = update.message.text
    if not text:
        return

    # 1. Check Sudo Password Flow
    if is_awaiting_sudo():
        action = get_pending_sudo_action()
        set_sudo_password(text)
        
        if action == "SYSTEM_RESTART":
            success, error = execute_with_sudo(["reboot"])
            if success:
                await update.message.reply_text("🔄 Rebooting system now...")
            else:
                await update.message.reply_text(f"❌ Reboot failed: {error}")
        elif action == "SYSTEM_LOGOUT":
            success, error = execute_with_sudo(["gnome-session-quit", "--logout", "--no-prompt"])
            if success:
                await update.message.reply_text("👋 Logging out...")
            else:
                await update.message.reply_text(f"❌ Logout failed: {error}")
        return

    # 2. Check Screen Lock Password Flow
    if is_awaiting_password():
        set_password(text)
        success = inject_password()
        if success:
            await update.message.reply_text("🔑 Password injected and wiped from memory.")
        else:
            await update.message.reply_text("❌ Failed to inject password.")
        return

    # 3. Check Skill Password Flow
    if is_awaiting_skill_password(user.id):
        await verify_skill_password(update, context)
        return

    # 4. Standard Antigravity Injection
    await core_handle_message(update, context)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle Inline Button clicks."""
    query = update.callback_query
    await query.answer() # Acknowledge click

    data = query.data
    user_id = query.from_user.id
    
    # Handle Model Selection buttons
    if data.startswith("MODEL:"):
        await handle_model_selection(query)
        return
    elif data.startswith("SKILL:"):
        await handle_skill_selection(query)
        return
    elif data == "CLICK_MODEL_DROPDOWN":
        from antigravity.model_selector import click_model_dropdown
        await query.edit_message_text("🖱️ Clicking model selector in UI...")
        success, model = click_model_dropdown()
        if success:
            await query.message.reply_text(f"✅ Clicked model selector. Current model: {model}")
        else:
            await query.message.reply_text("❌ Failed to click model selector.")
        return
    
    # Handle Accept/Reject ALL buttons
    if data == "ACCEPT_ALL":
        await handle_accept_all(query)
        return
    elif data == "REJECT_ALL":
        await handle_reject_all(query)
        return
    
    # Handle Allow Access buttons
    if data == "ALLOW_ONCE":
        await handle_allow_access(query, "allow_once")
        return
    elif data == "ALLOW_CONV":
        await handle_allow_access(query, "allow_conv")
        return
    
    # Handle confirmation buttons (existing logic)
    if ":" not in data:
        return

    decision, action = data.split(":", 1)
    
    # Resolve against pending
    result = resolve_confirmation(user_id, decision)
    
    if result:
        await query.edit_message_text(f"✅ Action confirmed: {result}")
        
        # Dispatch execution
        if result == "SYSTEM_RESTART":
            await execute_system_restart(update, context)
        elif result == "SYSTEM_LOGOUT":
            await execute_system_logout(update, context)
        else:
            await query.message.reply_text(f"⚠️ Action '{result}' confirmed but no handler found.")
            
    else:
        # Either cancelled (NO) or expired/invalid
        if decision == "NO":
            await query.edit_message_text(f"❌ Action cancelled: {action}")
        else:
            await query.edit_message_text("⚠️ Confirmation expired or invalid.")

async def handle_model_selection(query):
    """Handle model selection button click."""
    from antigravity.model_selector import select_model_by_name
    
    # Extract model name from callback data
    model_name = query.data.replace("MODEL:", "")
    
    await query.edit_message_text(f"🔄 Switching to {model_name}...")
    
    # Click the model in Antigravity UI and check for limits
    success, is_limited, message = select_model_by_name(model_name)
    
    if success:
        if is_limited:
            await query.message.reply_text(f"⚠️ **{model_name} Selected**\n\n{message}\n\nYou may need to switch to a different model if it stops responding.")
        else:
            await query.message.reply_text(f"✅ **{model_name} Selected**\n\nThe AI model has been successfully updated.")
    else:
        await query.message.reply_text(f"❌ **Switch Failed**\n\n{message}\n\nMake sure Antigravity is visible on your screen.")


async def handle_accept_all(query):
    """Click Accept ALL button in Antigravity UI."""
    from antigravity.button_mapper import detect_action_buttons, click_button
    
    await query.edit_message_text("🔍 Detecting Accept button in Antigravity...")
    
    buttons = detect_action_buttons()
    if buttons and "accept_all" in buttons:
        success = click_button(buttons["accept_all"])
        if success:
            await query.message.reply_text("✅ Clicked Accept ALL in Antigravity UI")
        else:
            await query.message.reply_text("❌ Failed to click Accept button")
    else:
        await query.message.reply_text("⚠️ Accept ALL button not found in Antigravity UI. Make sure the changes are visible.")

async def handle_reject_all(query):
    """Click Reject ALL button in Antigravity UI."""
    from antigravity.button_mapper import detect_action_buttons, click_button
    
    await query.edit_message_text("🔍 Detecting Reject button in Antigravity...")
    
    buttons = detect_action_buttons()
    if buttons and "reject_all" in buttons:
        success = click_button(buttons["reject_all"])
        if success:
            await query.message.reply_text("❌ Clicked Reject ALL in Antigravity UI")
        else:
            await query.message.reply_text("❌ Failed to click Reject button")
    else:
        await query.message.reply_text("⚠️ Reject ALL button not found in Antigravity UI. Make sure the changes are visible.")

async def security_monitor(context: ContextTypes.DEFAULT_TYPE):
    """Background job to detect password prompts, access requests, and quota limits."""
    user_id = os.getenv("TELEGRAM_USER_ID")
    if not user_id:
        return

    # 1. Check for Password Prompts
    if not is_awaiting_password():
        if detect_password_prompt():
            set_awaiting_password(True)
            await context.bot.send_message(
                chat_id=user_id, 
                text="🔑 **KEYRING AUTHENTICATION REQUIRED**\n\nA system keyring or authentication prompt has been detected.\n\nSend your password and I'll auto-paste it into the input box for you."
            )

    # 2. Check for Directory Access Prompts (Allow Once / Allow Conversation)
    from antigravity.button_mapper import detect_action_buttons
    buttons = detect_action_buttons()
    if buttons and ("allow_once" in buttons or "allow_conv" in buttons):
        from telegram_interface.ui import allow_access_keyboard
        # Check if we already alerted (simple rate limit using job_data)
        last_alert = context.job.data.get("last_access_alert", 0) if context.job.data else 0
        import time
        if time.time() - last_alert > 60: # Alert once per minute
            if context.job.data is None: context.job.data = {}
            context.job.data["last_access_alert"] = time.time()
            
            await context.bot.send_message(
                chat_id=user_id,
                text="🛡️ **DIRECTORY ACCESS REQUESTED**\n\nAntigravity is asking for permission to access your files.\n\nChoose an option below:",
                reply_markup=allow_access_keyboard()
            )

    # 3. Check for AI Quota Limits (PROACTIVE)
    from antigravity.quota_detector import detect_quota_popup
    btn_coords, limit_model = detect_quota_popup()
    if btn_coords:
        last_limit_alert = context.job.data.get("last_limit_alert", 0) if context.job.data else 0
        import time
        if time.time() - last_limit_alert > 300: # Alert once per 5 mins
            if context.job.data is None: context.job.data = {}
            context.job.data["last_limit_alert"] = time.time()
            
            await context.bot.send_message(
                chat_id=user_id,
                text=f"⚠️ **AI QUOTA REACHED**\n\nThe current model (**{limit_model}**) has hit its usage limit.\n\nUse /select_model to switch to another model now.",
                parse_mode="Markdown"
            )

async def post_init(application):
    """Setup commands menu in Telegram."""
    commands_list = []
    for cmd, desc in COMMAND_DESCRIPTIONS.items():
        commands_list.append(BotCommand(cmd, desc))
    
    await application.bot.set_my_commands(commands_list)
    logger.info("Bot command menu initialized.")

def run_bot():
    if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("❌ No valid TELEGRAM_BOT_TOKEN found in config/secrets.env")
        return

    application = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    
    # Register commands
    for cmd_triggers in COMMANDS.keys():
        command_name = cmd_triggers.lstrip("/")
        application.add_handler(CommandHandler(command_name, route_command))

    # Register Message Handler (Wrapped)
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message_wrapper))
    
    # Register Callback Handler (Buttons)
    application.add_handler(CallbackQueryHandler(button_handler))

    # Register Background Jobs
    if application.job_queue:
        application.job_queue.run_repeating(security_monitor, interval=10, first=5)

    print("🦅 CLAWBOLT Bot is polling...")
    application.run_polling()

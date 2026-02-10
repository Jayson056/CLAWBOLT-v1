# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram_interface.auth import is_authorized

logger = logging.getLogger(__name__)


async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show available commands."""
    user = update.effective_user
    if not user or not is_authorized(user.id):
        return

    rules_text = """
⚡ **CLAWBOLT COMMAND CENTER**

**🎯 Getting Started**
`/start` - Verify CLAWBOLT connectivity
`/help` or `/rules` - Show this command list

**🔧 System Control**
`/restart` - Restart Antigravity AI interface
`/sysrest` - Restart entire system (needs confirmation)
`/syslogout` - Log out session (needs confirmation)

**📸 Screen & Monitoring**
`/screen` - Capture and send current screenshot
`/watch` - Monitor screen for changes
`/report` - Get system status report

**🤖 AI Interface**
`/quota` - Check AI model usage limits
`/select_model` - Interactive model selection
`/select_skill` - Switch AI persona/skills mode
`/accept` - Click "Accept ALL" in Antigravity
`/reject` - Click "Reject ALL" in Antigravity
`/pass <password>` - Send password for keyring

**📁 File System**
`/ls [path]` - List directory contents
`/save` - Save conversation snapshot

**🎧 Audio**
`/hear` - Listen to last 10s of system audio

**💡 Key Features:**
• 🧠 **Skill Modes**: Toggle between Workspace, School, Maintenance, etc.
• 🎛️ **Interactive UI**: Accept/Reject buttons for file changes
• 🔐 **Secure Flow**: Auto-detection of password prompts
• 👁️ **Visual Intelligence**: OCR-based model & quota detection
• 🎙️ **Dual-Mode**: Every AI response includes Text + Voice

**Available Skills Menu (/select_skill):**
• 🛠️ Core Maintenance (Auth Required)
• 🏢 Workspace (Default)
• 🎓 School & Student Modes
• 🔬 Research & Programming Expert
• ✍️ Creative & Data Analyst

_CLAWBOLT v2.0 - Bridging Telegram with Antigravity AI_
    """
    try:
        await update.message.reply_markdown(rules_text)
    except Exception as e:
        logger.error(f"Failed to send rules: {e}")
        # Fallback to plain text if markdown fails
        await update.message.reply_text(rules_text.replace("*", "").replace("_", ""))
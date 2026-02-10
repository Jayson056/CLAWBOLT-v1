# CLAWBOLT

**CLAWBOLT** is a secure, Telegram-driven control system for Antigravity AI and Linux system automation, designed with strict **Human-in-the-Loop** execution.

**Created by Jayson056**
**Copyright © 2026 Jayson056. All rights reserved.**

## 1. Project Rationale
CLAWBOLT is designed to bridge human authority, AI assistance, and system-level automation in a controlled, observable, and reversible way. Modern AI tools can reason, but must not act without consent when actions involve file access, system modification, or privileged commands.

This architecture ensures:
- **Accountability**: Users sign off on actions.
- **Transparency**: Every action is visible.
- **Auditability**: Logs and screenshots track behavior.
- **Safety**: No silent execution.

## 2. Features
- **Real-time AI Interaction**: Chat with Antigravity AI via Telegram.
- **Smart Quota Awareness**: Check AI limits (`/quota`).
- **Project Portability**: Export full project snapshots (`/save`).
- **System Power Control**: Restart (`/sysrest`) and Logout (`/syslogout`).
- **Media Tools**: Record screen (`/watch`) and audio (`/hear`).
- **Security**: 
  - **Inline Buttons**: Tap-based confirmation for critical actions.
  - **Password Flow**: Securely inject passwords memory-only.
  - **Auto-Start**: Systemd service resilience.

## 3. Work Breakdown Structure (WBS)
### Phase 1 — Control Plane
- Telegram bot, User auth, Command routing.
### Phase 2 — AI Integration
- Antigravity UI automation, Injection logic.
### Phase 3 — Verification Layer
- Action classification, Inline approval UI.
### Phase 4 — Resilience & Expansion
- Media commands, System status.
### Phase 5 — Privilege Control
- Sudo proxy, Password handling, Secure execution.
### Phase 6 — Deployment & Hardening
- Systemd service, Sudoers hardening, Documentation.

## 4. Requirements
- Linux Mint 22.3 (or compatible)
- Python 3.10+
- Telegram Bot Token
- Antigravity AI installed locally

## 5. Startup
```bash
# Manual Start
source .venv/bin/activate
python3 main.py

# Auto-Start (after install)
sudo systemctl start clawbolt
```

## 6. Safety Model
- **No Silent Execution**: Every destructive action requires explicit confirmation.
- **Transient Auth**: Passwords are wiped from memory immediately after use.
- **Full Observability**: Screenshot and log everything.

## 7. Disclaimer
**CLAWBOLT is designed for authorized systems only.**
The user retains full responsibility for all executed actions.

---
**AI assists. Humans decide. Systems obey.**

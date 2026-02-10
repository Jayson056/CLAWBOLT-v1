# 🦅 CLAWBOLT - Private AI Control Bridge

**CLAWBOLT** is a secure, Telegram-driven control system for Antigravity AI and Linux system automation. It implements a strict **Human-in-the-Loop** (HITL) execution model, ensuring that while AI can reason and recommend, only the human user can authorize high-stakes actions.

---

## 📖 Project Overview
CLAWBOLT serves as the secure interface between a remote user and a local Linux machine running Antigravity AI. It handles authentication, secure password injection, screen monitoring, and remote system management through a polished Telegram interface.

### Core Philosophy
- **AI-Assisted, Human-Decided**: No destructive action happens without user confirmation via secure inline buttons.
- **Privacy First**: Sensitive data like passwords are never stored; they are injected directly into system memory/input buffers and wiped.
- **Resilient Execution**: Designed to run as a system service with auto-recovery.

---

## 📂 Documentation & Architecture
Full documentation is organized into phases and specific guides:

- **[Installation & Requirements](docs/instruction.md)**: Detailed machine requirements and setup guide.
- **Project Structure**:
    - `/docs`: Contains phase-by-phase development documentation, WBS, and rationale.
    - `/agent`: Higher-level intelligence routing.
    - `/antigravity`: UI-specific mapping for the Antigravity AI interface.
    - `/security`: Validation layers and secure credential flows.

> **Note for Developers**: Please refer to the `docs/` directory for technical deep-dives into each implementation phase. Start with `docs/instruction.md` for machine setup.

---

## 🎯 Project Rationale
Modern AI tools are increasingly capable of performing system-level actions. However, autonomous execution on personal machines carries extreme risks. CLAWBOLT was created to:
1. Provide a **secure tunnel** for system interaction.
2. Implement **visual verification** (screenshots/watchdogs) so the user sees what the AI sees.
3. Enforce **explicit consent** for every file move, command execution, or system change.

---

## 🏗️ Work Breakdown Structure (WBS)
- **Phase 1: Control Plane** (Bot initialization, Auth, Core routing)
- **Phase 2: AI Integration** (UI mapping, Text injection)
- **Phase 3: Verification Layer** (Action classification, Dynamic approval UI)
- **Phase 4: Media & Resilience** (Screen recording, System telemetry)
- **Phase 5: Privilege Escalation** (Secure sudo proxy, Memory-safe password injection)
- **Phase 6: Deployment** (Systemd hardening, Documentation)

---

## 🚀 Quick Start
Refer to **[docs/instruction.md](docs/instruction.md)** for detailed setup.

```bash
# Basic run
source .venv/bin/activate
python3 main.py
```

---

## 🛡️ Safety Model
- **No Shadow Execution**: Transparent logs and real-time screen updates.
- **Volatile Secrets**: Tokens and passwords remain in memory only as long as needed.
- **Locked Scope**: Execution limited to predefined safe zones unless explicitly expanded.

---
Created by **Jayson056** | Copyright © 2026. All rights reserved.

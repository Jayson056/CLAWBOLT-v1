# CLAWBOLT Machine Requirements & Installation Instructions

This document provides everything you need to set up the host machine and install CLAWBOLT.

## 1. Machine Requirements

### Operating System
- **Linux** (Tested on Linux Mint 22.3 "Wilma")
- **Desktop Environment**: GNOME/Cinnamon (required for UI automation)
- **Display**: X11 (PyAutoGUI support)

### Hardware Minimums
- **CPU**: Dual-core 2.0GHz+
- **RAM**: 4GB (8GB recommended for Antigravity AI)
- **Disk**: 500MB for logs and snapshots

### Software Dependencies
- **Python**: 3.10 or higher
- **OCR**: Tesseract OCR (`sudo apt install tesseract-ocr`)
- **System Tools**: `scrot`, `ffmpeg`, `sox` (if audio features used)
- **Privileged Access**: Sudo rights for installation and system commands

---

## 2. Pre-Installation Setup

### 1. Create a Telegram Bot
1. Message [@BotFather](https://t.me/botfather) on Telegram.
2. Create a new bot and copy the **API Token**.
3. Use [@userinfobot](https://t.me/userinfobot) to get your **Telegram User ID**.

### 2. Prepare Environment
Install system-level dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv tesseract-ocr scrot xdotool
```

---

## 3. Installation Steps

### 1. Clone & Setup Virtual Environment
```bash
git clone https://github.com/yourusername/CLAWBOLT-v1.git
cd CLAWBOLT-v1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Secrets
Create a `config/secrets.env` file (this file is gitignored):
```bash
TELEGRAM_BOT_TOKEN="your_bot_token_here"
TELEGRAM_USER_ID="your_user_id_here"
```

### 3. Sudoers Configuration (Optional but Recommended)
To allow `/sysrest` and `/syslogout` without manual password entry in the terminal:
```bash
sudo cp deployment/clawbolt_sudoers /etc/sudoers.d/clawbolt
sudo chmod 440 /etc/sudoers.d/clawbolt
```

---

## 4. Running the Application

### Manual Start
```bash
source .venv/bin/activate
python3 main.py
```

### Systemd Service (Recommended)
1. Copy the service file:
   ```bash
   sudo cp deployment/clawbolt.service /etc/systemd/system/
   ```
2. Reload and Start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable clawbolt
   sudo systemctl start clawbolt
   ```

---

## 5. Directory Overview
- `agent/`: AI command logic and UI automation.
- `antigravity/`: Antigravity-specific screen mapping and detectors.
- `config/`: Configuration files and secrets management.
- `docs/`: Expanded documentation (Requirement: See `instruction.md`).
- `telegram_interface/`: Bot handlers and UI components.
- `utils/`: Core utilities for networking and system interactions.

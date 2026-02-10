# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
import logging
import os
import sys
import atexit
import asyncio
from datetime import datetime
from telegram_interface.bot import run_bot
from utils.startup import send_startup_notification
from core.watcher import start_watcher, wait_for_antigravity

from core.security import check_core_integrity

# Ensure DISPLAY is set for GUI operations (even when running as service)
if "DISPLAY" not in os.environ:
    os.environ["DISPLAY"] = ":0"

# --- READ-ONLY RUNTIME CHECK (Self-Defense) ---
if not check_core_integrity():
    print("\n⚠️  [SECURITY ALERT] CLAWBOLT core is writable — unsafe state")
# -----------------------------------------------
if "XAUTHORITY" not in os.environ:
    os.environ["XAUTHORITY"] = "/home/son/.Xauthority"
if "XDG_RUNTIME_DIR" not in os.environ:
    os.environ["XDG_RUNTIME_DIR"] = "/run/user/1000"

# Paths
LOG_DIR = "Debug/Console"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def setup_logging():
    """Sets up logging to console and file."""
    # Create a unique temp filename for this session
    start_time = datetime.now()
    start_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    temp_log_file = os.path.join(LOG_DIR, f"current_session_{start_time.strftime('%Y%m%d_%H%M%S')}.log")

    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),  # Log to console
            logging.FileHandler(temp_log_file, mode='w', encoding='utf-8')  # Log to file
        ]
    )
    
    return temp_log_file, start_str

def finalize_log(temp_file, start_str):
    """Renames the temp log file to include end time."""
    if not os.path.exists(temp_file):
        return

    end_time = datetime.now()
    end_str = end_time.strftime("%Y-%m-%d %H:%M:%S")
    
    # New filename: consoleLog-<start> to <end>.txt
    # Filesystems usually dislike ':' in filenames on Windows, but Linux is okay.
    # To be safe and cleaner, let's format timestamps slightly differently or keep it if user insists.
    # User requested: "consoleLog with date satrt and end date"
    # Example: consoleLog-2023-10-27_10-00-00_to_2023-10-27_10-05-00.txt
    
    safe_start = start_str.replace(":", "-").replace(" ", "_")
    safe_end = end_str.replace(":", "-").replace(" ", "_")
    
    final_name = f"consoleLog-{safe_start}_to_{safe_end}.txt"
    final_path = os.path.join(LOG_DIR, final_name)
    
    try:
        os.rename(temp_file, final_path)
        print(f"\n📝 Log saved to: {final_path}")
    except OSError as e:
        print(f"\n❌ Failed to save log: {e}")

if __name__ == "__main__":
    # Setup logging
    temp_log, start_str = setup_logging()
    
    # Register cleanup handler
    atexit.register(finalize_log, temp_log, start_str)
    
    # Start Antigravity watcher (waits and auto-restarts)
    print("🔍 Starting Antigravity watcher...")
    start_watcher()
    
    # Wait for Antigravity to be ready before sending notification
    print("⏳ Waiting for Antigravity...")
    antigravity_ready = wait_for_antigravity(timeout=120)
    
    # Send startup notification
    if antigravity_ready:
        try:
            asyncio.run(send_startup_notification())
        except Exception as e:
            print(f"⚠️ Notification failed: {e}")
    else:
        print("⚠️ Starting without Antigravity (will retry in background)")
    
    # Run the bot
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        logging.error(f"Fatal Error: {e}")
        print(f"\n❌ Fatal Error: {e}")

# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
import subprocess
import logging

logger = logging.getLogger(__name__)

def focus_antigravity(window_name="Antigravity"):
    """
    Bring the Antigravity window to the foreground using wmctrl.
    Returns True if successful, False otherwise.
    """
    try:
        # Try finding "Antigravity"
        subprocess.run(
            ["wmctrl", "-a", window_name],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        logger.info(f"Focused window: {window_name}")
        return True
    except subprocess.CalledProcessError:
        # Fallback: Try "CLAWBOLT" or "Walkthrough" since the user has those windows
        logger.warning(f"Window '{window_name}' not found. Trying fallbacks.")
        fallback_names = ["CLAWBOLT", "Walkthrough", "Mozilla Firefox"] # detected from wmctrl
        for name in fallback_names:
            try:
                subprocess.run(
                    ["wmctrl", "-a", name],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                logger.info(f"Focused fallback window: {name}")
                return True
            except subprocess.CalledProcessError:
                continue
        
def get_antigravity_geometry(window_name="Antigravity"):
    """
    Returns (x, y, width, height) of the Antigravity window.
    """
    try:
        output = subprocess.check_output(["wmctrl", "-lG"], text=True)
        for line in output.splitlines():
            if window_name.lower() in line.lower():
                parts = line.split()
                # format: id desktop x y w h host name
                return int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5])
        return None
    except Exception as e:
        logger.error(f"Failed to get window geometry: {e}")
        return None

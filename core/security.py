# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
import os
import logging

logger = logging.getLogger(__name__)

# Define immutable core and mutable workspace
CLAWBOLT_ROOT = "/home/son/CLAWBOLT"
ALLOWED_PATHS = [
    "/home/son/CLAWBOLT_Workspaces",
    "/home/son/CLAWBOLT/storage",
    "/tmp",
    "/var/lib/clawbolt"
]

def is_maintenance_mode():
    """
    Checks if the system is in maintenance mode.
    """
    return os.path.exists(os.path.join(CLAWBOLT_ROOT, ".maintenance"))

def is_allowed_path(path):
    """
    Checks if a given path is within the allowed mutable workspaces.
    """
    if is_maintenance_mode():
        return True # All paths allowed in maintenance mode

    abs_path = os.path.abspath(path)
    
    # Check if it's in allowed paths
    is_allowed = any(abs_path.startswith(os.path.abspath(p)) for p in ALLOWED_PATHS)
    
    # Explicitly block core code edits even if somehow nested (safety first)
    # We block .py files, .sh files, and hidden config dirs in the core root
    if abs_path.startswith(os.path.abspath(CLAWBOLT_ROOT)):
        # Exceptions for storage/ logs/ etc are handled by ALLOWED_PATHS check above
        # If it's NOT in ALLOWED_PATHS but IS in CLAWBOLT_ROOT, it's core
        if not is_allowed:
            return False

    return is_allowed

def check_core_integrity():
    """
    Checks if the CLAWBOLT core directory is writable.
    Returns True if safe (read-only), False if unsafe (writable).
    """
    if os.access(CLAWBOLT_ROOT, os.W_OK):
        logger.warning(f"SECURITY ALERT: CLAWBOLT core ({CLAWBOLT_ROOT}) is writable!")
        return False
    return True

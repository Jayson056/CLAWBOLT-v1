# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
import logging
import subprocess

logger = logging.getLogger(__name__)

# In-memory sudo password state
_sudo_password = None
_awaiting_sudo = False
_pending_sudo_action = None  # Stores which action to retry (SYSTEM_RESTART, SYSTEM_LOGOUT)

def set_awaiting_sudo(action: str) -> None:
    """Sets the state to awaiting sudo password for a specific action."""
    global _awaiting_sudo, _pending_sudo_action
    _awaiting_sudo = True
    _pending_sudo_action = action
    logger.info(f"Awaiting sudo password for: {action}")

def is_awaiting_sudo() -> bool:
    """Checks if the system is awaiting sudo password input."""
    return _awaiting_sudo

def get_pending_sudo_action() -> str | None:
    """Returns the pending sudo action."""
    return _pending_sudo_action

def set_sudo_password(password: str) -> None:
    """Temporarily stores sudo password in memory."""
    global _sudo_password
    _sudo_password = password

def execute_with_sudo(command: list[str]) -> tuple[bool, str]:
    """
    Executes a command with sudo using the stored password.
    Returns (success: bool, error_message: str)
    """
    global _sudo_password, _awaiting_sudo, _pending_sudo_action
    
    if not _sudo_password:
        return False, "No password provided"
    
    try:
        # Use echo to pipe password to sudo -S
        full_command = f"echo '{_sudo_password}' | sudo -S {' '.join(command)}"
        result = subprocess.run(
            full_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Check if it failed due to wrong password
        if result.returncode != 0 and ("password" in result.stderr.lower() or "sorry" in result.stderr.lower()):
            return False, "Incorrect password"
        
        return True, ""
        
    except subprocess.TimeoutExpired:
        return False, "Command timeout"
    except Exception as e:
        logger.error(f"Sudo execution failed: {e}")
        return False, str(e)
    finally:
        # CRITICAL: Wipe password from memory
        _sudo_password = None
        _awaiting_sudo = False
        _pending_sudo_action = None

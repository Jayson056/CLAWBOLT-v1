# Phase 5: Privilege Control & Secure Injection

## Objectives
- Handle sensitive system prompts (sudo, keyring).
- Implement memory-safe password injection.
- Secure terminal command execution.

## Key Components
- **Password Flow**: Detecting authentication prompts and requesting the password via a secure Telegram message.
- **Sudo Proxy**: Allowing specific reboot/logout actions via `/etc/sudoers.d/clawbolt`.
- **Volatile Storage**: Ensuring secrets are wiped after a single use.

## Technical Details
- Using `pyautogui.write` for character-by-character injection to bypass some clipboard monitors.
- Permission hardening for deployment scripts.

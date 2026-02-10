# Phase 2: AI Integration & UI Automation

## Objectives
- Connect Telegram inputs to the local Antigravity AI interface.
- Automate text injection into the AI input box.
- Map UI elements for programmatic interaction.

## Key Components
- **UI Mapper**: Identifying coordinates for "Ask anything" input boxes.
- **PyAutoGUI Bridge**: Simulating keyboard and mouse events to interact with the persistent AI window.
- **Context Injection**: Handling multi-line prompts and maintaining focus.

## Technical Details
- Threshold-based pixel matching for button detection.
- Focus-stealing prevention during injection.

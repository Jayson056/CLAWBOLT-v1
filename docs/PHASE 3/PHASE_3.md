# Phase 3: Verification Layer & HITL

## Objectives
- Implement Human-in-the-Loop (HITL) for critical actions.
- Use Telegram Inline Buttons for quick approvals.
- Prevent autonomous execution of sensitive commands.

## Key Components
- **Action Classifier**: Distinguishing between safe "read-only" queries and "system-modifying" actions.
- **Confirmation Flow**: intercepting commands and requiring a 'YES' click before proceeding.
- **Job Queue**: Managing pending confirmations with expiry.

## Technical Details
- Callback query handlers for efficient button-click processing.
- State management for pending user decisions.

# Phase 4: Media Monitoring & Resilience

## Objectives
- Provide real-time visual feedback to the remote user.
- Capture screen snapshots and audio logs.
- Monitor AI state transitions (quota limits, errors).

## Key Components
- **Screen Watcher (`/watch`)**: capturing high-quality JPEG screenshots.
- **Audio Monitor (`/hear`)**: Recording system audio snippets.
- **Quota Detector**: Proactively scanning the screen for "Quota Reached" popups and alerting the user.

## Technical Details
- Background threads for continuous monitoring without blocking the bot.
- Adaptive JPEG compression to balance detail and transfer speed.

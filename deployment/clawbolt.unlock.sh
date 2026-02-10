#!/bin/bash
# CLAWBOLT Core Unlocking Script

echo "🔓 CLAWBOLT: Entering Maintenance Mode"

CLAWBOLT_CORE="/home/son/CLAWBOLT"

sudo chown -R son:son "$CLAWBOLT_CORE"
sudo chmod -R 775 "$CLAWBOLT_CORE"

# Create maintenance flag file
touch "$CLAWBOLT_CORE/.maintenance"

echo "✅ Core unlocked for maintenance/upgrades."
echo "⚠️  Remember to run 'clawbolt.lock.sh' when finished!"

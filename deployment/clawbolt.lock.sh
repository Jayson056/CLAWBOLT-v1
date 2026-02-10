#!/bin/bash
# CLAWBOLT Core Locking Script
# Inspired by CLAWBOLT DOCUMENTATION FINAL PHASE 1.1 REFACTORING.pdf

echo "🔐 CLAWBOLT Phase 1.1: Final Hardening"

# 1. Create dedicated system user
echo "👤 Creating dedicated system user 'clawbolt'..."
sudo useradd -r -s /usr/sbin/nologin clawbolt || echo "User 'clawbolt' already exists."

# 2. Define Paths
CLAWBOLT_CORE="/home/son/CLAWBOLT"
CLAWBOLT_WORKSPACES="/home/son/CLAWBOLT_Workspaces"

# 3. Ownership and Permissions for Core
echo "🛡️  Locking CLAWBOLT Core (read-only)..."
sudo chown -R root:root "$CLAWBOLT_CORE"
sudo chmod -R 755 "$CLAWBOLT_CORE"
sudo chmod -R a-w "$CLAWBOLT_CORE"

# Allow specific core subdirectories to be writable by root (for maintenance)
# and ensure log/storage dirs are accessible if needed.
# However, the security policy says storage should be in ALLOWED_PATHS.
sudo chmod -R 777 "$CLAWBOLT_CORE/storage" # Ensure storage is writable for the app
sudo chown -R clawbolt:clawbolt "$CLAWBOLT_CORE/storage"
sudo chmod -R 777 "$CLAWBOLT_CORE/Debug"
sudo chown -R clawbolt:clawbolt "$CLAWBOLT_CORE/Debug"

# 4. Workspace Access Control
echo "📂 Setting up Workspace access for 'clawbolt' user..."
sudo chown -R son:son "$CLAWBOLT_WORKSPACES" # User 'son' owns workspaces
sudo chmod -R 775 "$CLAWBOLT_WORKSPACES"
# Give clawbolt user read-execute access to workspaces via ACL
sudo setfacl -R -m u:clawbolt:rx "$CLAWBOLT_WORKSPACES"

# 5. GUI Access (Crucial for Antigravity bridge)
echo "🖥️  Configuring GUI access for 'clawbolt' user..."
sudo setfacl -m u:clawbolt:r /home/son/.Xauthority
sudo setfacl -R -m u:clawbolt:rwx /run/user/1000

# 6. Systemd Service Update
echo "🔄 Updating systemd service..."
SERVICE_FILE="/home/son/CLAWBOLT/deployment/clawbolt.service"
sudo sed -i 's/User=son/User=clawbolt/' "$SERVICE_FILE"
sudo sed -i 's/Group=son/Group=clawbolt/' "$SERVICE_FILE" || echo "Group already correct or not found."

echo "✅ Hardening complete!"
echo "🚀 Run 'sudo systemctl daemon-reload && sudo systemctl restart clawbolt' to apply."

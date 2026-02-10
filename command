[Unit]
Description=CLAWBOLT Control Agent
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=son
Group=son
WorkingDirectory=/home/son/CLAWBOLT

# Environment variables to support the GUI/X11 hooks in main.py
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/son/.Xauthority
Environment=XDG_RUNTIME_DIR=/run/user/1000
Environment=PYTHONUNBUFFERED=1
Environment=PYTHONPATH=/home/son/CLAWBOLT

# Executing using the virtual environment
ExecStart=/home/son/CLAWBOLT/.venv/bin/python3 /home/son/CLAWBOLT/main.py

# Restart logic
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target



# Reload the systemd daemon to pick up the changes
sudo systemctl daemon-reload

# Restart the service
sudo systemctl restart clawbolt

# Check status immediately
systemctl status clawbolt

# View the real-time Python traceback if it still crashes
sudo journalctl -u clawbolt.service -f

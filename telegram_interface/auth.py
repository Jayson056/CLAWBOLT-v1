# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="config/secrets.env")

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Allowed user IDs
ALLOWED_USER_ID = int(os.getenv("TELEGRAM_USER_ID", 0))

def is_authorized(user_id: int) -> bool:
    """Check if the user is authorized to use the bot."""
    if user_id == ALLOWED_USER_ID:
        return True
    logger.warning(f"Unauthorized access attempt by user ID: {user_id}")
    return False

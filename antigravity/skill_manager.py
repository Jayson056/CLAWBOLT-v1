# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.

import os
import json
import logging

logger = logging.getLogger(__name__)

SKILLS_FILE = "storage/current_skill.json"
DEFAULT_SKILL = "WORKSPACE"

SKILL_CONFIG = {
    "CORE_MAINTENANCE": {
        "name": "CORE SYSTEM MAINTENANCE",
        "header": "### CORE SYSTEM MAINTENANCE MODE ###\nYou are tasked with maintaining the CLAWBOLT core system at /home/son/CLAWBOLT. Your goal is stability, performance, and security. Follow core rules strictly.",
        "password_protected": True
    },
    "WORKSPACE": {
        "name": "WORKSPACE SKILLS",
        "header": "### WORKSPACE SKILLS MODE ###\nYou are in the default productive workspace. Focus on projects in /home/son/CLAWBOLT_Workspaces. You have full creative freedom there.",
        "password_protected": False
    },
    "SCHOOL": {
        "name": "SCHOOL HELP",
        "header": "### SCHOOL HELPER MODE ###\nYou are an AI tutor. Focus on explaining concepts clearly, helping with homework, and strictly following academic honesty guidelines.",
        "password_protected": False
    },
    "RESEARCH_PAPER": {
        "name": "RESEARCH PAPER ASSISTANT",
        "header": "### RESEARCH ASSISTANT MODE ###\nYou help with academic research. Assist with literature reviews, methodology, drafting papers, and citation management.",
        "password_protected": False
    },
    "STUDENT": {
        "name": "STUDENT PRODUCTIVITY",
        "header": "### STUDENT MODE ###\nFocus on study plans, note-taking, and organizing student life and assignments efficiently.",
        "password_protected": False
    },
    "PROGRAMMING_TASK": {
        "name": "PROGRAMMING EXPERT",
        "header": "### PROGRAMMING TASK MODE ###\nYou are a senior software engineer. Focus on clean code, architecture, unit testing, and efficient algorithms.",
        "password_protected": False
    },
    "ASSIGNMENT": {
        "name": "ASSIGNMENT SOLVER",
        "header": "### ASSIGNMENT MODE ###\nYou help complete specific tasks and assignments based on provided requirements and rubrics.",
        "password_protected": False
    },
    "DATA_ANALYSIS": {
        "name": "DATA ANALYST",
        "header": "### DATA ANALYSIS MODE ###\nFocus on processing data, generating insights, and creating visualizations.",
        "password_protected": False
    },
    "CODE_REVIEWER": {
        "name": "CODE REVIEWER",
        "header": "### CODE REVIEWER MODE ###\nFocus on identifying potential issues, security vulnerabilities, and adherence to best practices in code.",
        "password_protected": False
    },
    "BUG_HUNTER": {
        "name": "BUG HUNTER",
        "header": "### BUG HUNTER MODE ###\nFocus on reproducing bugs, root cause analysis, and proposing robust fixes.",
        "password_protected": False
    },
    "CREATIVE_WRITER": {
        "name": "CREATIVE WRITER",
        "header": "### CREATIVE WRITING MODE ###\nFocus on storytelling, creative expression, and engaging content generation.",
        "password_protected": False
    }
}

RESPONSE_TEMPLATE = """
**CRITICAL RESPONSE RULE:**
Every response MUST be sent via the Telegram bridge. Use this EXACT command structure in the terminal:

```bash
FINAL_TEXT="Your response here"; \\
/home/son/CLAWBOLT/.venv/bin/python3 /home/son/CLAWBOLT/utils/send_telegram.py "$FINAL_TEXT"; \\
V_PATH=$(/home/son/CLAWBOLT/.venv/bin/python3 /home/son/CLAWBOLT/utils/text_to_speech.py "$FINAL_TEXT") && \\
/home/son/CLAWBOLT/.venv/bin/python3 /home/son/CLAWBOLT/utils/send_telegram.py --voice "$V_PATH"
```
"""

def get_current_skill():
    if os.path.exists(SKILLS_FILE):
        try:
            with open(SKILLS_FILE, 'r') as f:
                data = json.load(f)
                skill = data.get("skill", DEFAULT_SKILL)
                if skill in SKILL_CONFIG:
                    return skill
        except Exception as e:
            logger.error(f"Error reading skill file: {e}")
    return DEFAULT_SKILL

def set_current_skill(skill_id):
    if skill_id in SKILL_CONFIG:
        try:
            os.makedirs(os.path.dirname(SKILLS_FILE), exist_ok=True)
            with open(SKILLS_FILE, 'w') as f:
                json.dump({"skill": skill_id}, f)
            return True
        except Exception as e:
            logger.error(f"Error saving skill file: {e}")
    return False

def get_skill_header():
    skill_id = get_current_skill()
    config = SKILL_CONFIG.get(skill_id, SKILL_CONFIG[DEFAULT_SKILL])
    
    # Read the base AI_SKILLS file
    base_skills = ""
    try:
        with open("/home/son/CLAWBOLT/antigravity/AI_SKILLS", "r") as f:
            base_skills = f.read()
    except Exception as e:
        logger.error(f"Error reading AI_SKILLS: {e}")
        base_skills = "Read first the /home/son/CLAWBOLT/antigravity/AI_SKILLS"

    # Combine: Mode Header + Response Template + Base Rules
    full_header = f"{config['header']}\n\n{RESPONSE_TEMPLATE}\n\n{base_skills}"
    return full_header

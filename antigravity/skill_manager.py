# CLAWBOLT - Created by Jayson056
# Copyright (c) 2026 Jayson056. All rights reserved.

import os
import logging

logger = logging.getLogger(__name__)

# Base directory for skill files
SKILLS_DIR = os.path.join(os.path.dirname(__file__), "AI_SKILLS_DIR")
STATE_FILE = os.path.join(os.path.dirname(__file__), "current_skill.txt")

SKILL_CONFIG = {
    "WORKSPACE": {
        "name": "Workspace Productivity", 
        "file": "WORKSPACE.skill",
        "mission": "Optimize workspace workflow, manage files, and automate daily tasks."
    },
    "SCHOOL": {
        "name": "School & Academic", 
        "file": "SCHOOL.skill",
        "mission": "Assist with general academic learning, note-taking, and educational research."
    },
    "STUDENT": {
        "name": "Student Tasks", 
        "file": "STUDENT.skill",
        "mission": "Help manage student schedules, reminders, and basic task execution."
    },
    "RESEARCH_PAPER": {
        "name": "Research Papers", 
        "file": "RESEARCH_PAPER.skill",
        "mission": "Deep-dive research, citation management, and academic synthesis."
    },
    "ASSIGNMENT": {
        "name": "Assignments", 
        "file": "ASSIGNMENT.skill",
        "mission": "Structured problem solving and content creation for course assignments."
    },
    "PROGRAMMING_TASK": {
        "name": "Programming Tasks", 
        "file": "PROGRAMMING_TASK.skill",
        "mission": "Code generation, algorithm optimization, and logical implementation."
    },
    "AI_ARCHITECT": {
        "name": "AI System Architect",
        "file": "AI_ARCHITECT.skill",
        "mission": "High-level design of AI workflows, agentic systems, and neural logic."
    },
    "CYBER_SECURITY": {
        "name": "Security Specialist",
        "file": "CYBER_SECURITY.skill",
        "mission": "Penetration testing, vulnerability scanning, and hardening of local systems."
    },
    "TECH_WRITER": {
        "name": "Technical Documentation",
        "file": "TECH_WRITER.skill",
        "mission": "Creating clear, concise, and structured technical docs and API guides."
    },
    "PROJECT_LEAD": {
        "name": "Project Management",
        "file": "PROJECT_LEAD.skill",
        "mission": "Timeline tracking, resource allocation, and project roadmap oversight."
    },
    "CORE_MAINTENANCE": {
        "name": "Core Maintenance", 
        "file": "CORE_MAINTENANCE.skill", 
        "password_protected": True,
        "mission": "Privileged system maintenance, updates, and low-level configuration."
    },
    "BUG_HUNTER": {
        "name": "Bug Hunter", 
        "file": "BUG_HUNTER.skill",
        "mission": "Identifying logical flaws, syntax errors, and runtime bottlenecks."
    },
    "CODE_REVIEWER": {
        "name": "Code Reviewer", 
        "file": "CODE_REVIEWER.skill",
        "mission": "Analyzing code quality, readability, and adherence to best practices."
    },
    "DATA_ANALYSIS": {
        "name": "Data Analysis", 
        "file": "DATA_ANALYSIS.skill",
        "mission": "Processing data sets, generating insights, and creating visual summaries."
    },
    "CREATIVE_WRITER": {
        "name": "Creative Writer", 
        "file": "CREATIVE_WRITER.skill",
        "mission": "Narrative drafting, storytelling, and imaginative content generation."
    },
}

def get_current_skill():
    """Returns the current active skill ID."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                skill_id = f.read().strip()
                if skill_id in SKILL_CONFIG:
                    return skill_id
        except Exception as e:
            logger.error(f"Error reading skill state: {e}")
    
    # Default skill
    return "WORKSPACE"

def set_current_skill(skill_id):
    """Sets the current active skill ID."""
    if skill_id not in SKILL_CONFIG:
        logger.error(f"Invalid skill ID: {skill_id}")
        return False
    
    try:
        with open(STATE_FILE, "w") as f:
            f.write(skill_id)
        return True
    except Exception as e:
        logger.error(f"Error saving skill state: {e}")
        return False

def get_skill_header():
    """Returns a premium structured header for the current active skill."""
    skill_id = get_current_skill()
    config = SKILL_CONFIG[skill_id]
    skill_file = os.path.abspath(os.path.join(SKILLS_DIR, config["file"]))
    core_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "AI_SKILLS"))
    
    status = "LOCKED" if config.get("password_protected") else "ACTIVE"
    
    header = f"🦅 [ SYSTEM: CLAWBOLT AI CORE ] 🦅\n"
    header += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    header += f"SKILL_NAME  : {config['name'].upper()}\n"
    header += f"MISSION     : {config['mission']}\n"
    header += f"STATUS      : {status}\n"
    header += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    header += f"SKILL_FILE  : {skill_file}\n"
    header += f"PERSONA_FILE: {core_file}\n"
    header += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    header += f"指令: 严格遵守上述文件定义的角色定位和运行策略。\n"
    
    return header

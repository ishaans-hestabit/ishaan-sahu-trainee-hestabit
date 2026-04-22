import os
from nexus_ai.config import LLM_CONFIG, WORKSPACE_DIR
from nexus_ai.agents.thinking import make_agent, THINKING_AGENTS
from nexus_ai.agents.code_agent import get_code_agent
from nexus_ai.agents.db_agent import get_db_agent
from nexus_ai.agents.file_agent import get_file_agent


def get_tool_agents():
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    return {
        "code": get_code_agent(LLM_CONFIG),
        "db": get_db_agent(LLM_CONFIG),
        "file": get_file_agent(LLM_CONFIG),
    }

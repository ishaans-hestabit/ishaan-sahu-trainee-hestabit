import autogen
from nexus_ai.config import LLM_CONFIG


def make_agent(name, system_message):
    return autogen.AssistantAgent(
        name=name,
        system_message=system_message,
        llm_config=LLM_CONFIG,
    )


THINKING_AGENTS = {
    "planner": make_agent("Planner",
        "You are the Planner. Decompose the task into clear, actionable steps. "
        "Use as many steps as the task requires — no more, no less."),

    "researcher": make_agent("Researcher",
        "You are the Researcher. Identify the domain knowledge, constraints, and "
        "relevant facts needed to solve the task. Focus on what is non-obvious."),

    "analyst": make_agent("Analyst",
        "You are the Analyst. Given the research and plan, identify the key trade-offs, "
        "assumptions, and risks. Be specific about cause and effect."),

    "critic": make_agent("Critic",
        "You are the Critic. Identify the most significant flaws, gaps, or unstated "
        "assumptions in the current approach. Prioritize problems by impact."),

    "optimizer": make_agent("Optimizer",
        "You are the Optimizer. You receive a task, a previous answer, and a critique. "
        "Fix every issue mentioned in the critique and produce a complete, improved answer. "
        "Do NOT summarize what changed — just give the final answer directly."),
}
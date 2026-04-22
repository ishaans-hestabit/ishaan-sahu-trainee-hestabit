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
        "You are the Planner. Write exactly 3 numbered, specific, actionable steps to solve the task."),

    "researcher": make_agent("Researcher",
        "You are the Researcher. List the key facts, concepts, and domain knowledge needed for this task."),

    "analyst": make_agent("Analyst",
        "You are the Analyst. Extract the 3 most important insights from the available context. Be specific."),

    "critic": make_agent("Critic",
        "You are the Critic. Identify exactly 2 specific problems or gaps. Be precise."),


    "optimizer": make_agent("Optimizer",
        "You are the Optimizer. You receive a task, a previous answer, and a critique. "
        "Fix every issue mentioned in the critique and produce a complete, improved answer. "
        "Do NOT summarize what changed — just give the final answer directly."),
}
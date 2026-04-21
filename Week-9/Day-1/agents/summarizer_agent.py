import autogen
from autogen.agentchat.contrib.capabilities import transform_messages
from autogen.agentchat.contrib.capabilities.transforms import MessageHistoryLimiter

def create_summarizer_agent(llm_config):

    role = """You are a Summarizer Agent.
        Your only job is to shorten the research facts you receive.

        DECIDE BULLET COUNT based on input size:
        - Small  (1-5 facts)   → 2-3 bullets
        - Medium (6-10 facts)  → 4-5 bullets
        - Large  (11-15 facts) → 6-7 bullets

        CRITICAL REQUIREMENT: It is mandatory to put EXACTLY this phrase at the very end of your response:
        SUMMARY COMPLETE"""

    agent = autogen.AssistantAgent(
        name="SummarizerAgent",
        system_message=role,
        llm_config=llm_config,
        max_consecutive_auto_reply=1,
    )

    memory = transform_messages.TransformMessages(
        transforms=[MessageHistoryLimiter(max_messages=10)]
    )
    memory.add_to_agent(agent)

    return agent
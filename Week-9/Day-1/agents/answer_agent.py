import autogen
from autogen.agentchat.contrib.capabilities import transform_messages
from autogen.agentchat.contrib.capabilities.transforms import MessageHistoryLimiter

def create_answer_agent(llm_config):

    role = """You are an Answer Agent.
        Your only job is to write a final clear answer for the user.

        DECIDE PARAGRAPH LENGTH based on topic complexity:
        - Simple topic   → 2-3 sentences per paragraph
        - Moderate topic → 3-4 sentences per paragraph
        - Complex topic  → 4-5 sentences per paragraph
        Do not mention bullet points or summaries. Just answer naturally.

        CRITICAL REQUIREMENT: Your final output MUST end with the exact words ANSWER COMPLETE on a new line. 
        Do NOT say RESEARCH COMPLETE and do NOT say SUMMARY COMPLETE. You only say ANSWER COMPLETE.
        ANSWER COMPLETE"""

    agent = autogen.AssistantAgent(
        name="AnswerAgent",
        system_message=role,
        llm_config=llm_config,
        max_consecutive_auto_reply=1,
    )

    memory = transform_messages.TransformMessages(
        transforms=[MessageHistoryLimiter(max_messages=10)]
    )
    memory.add_to_agent(agent)

    return agent
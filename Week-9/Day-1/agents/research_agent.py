import autogen
from autogen.agentchat.contrib.capabilities import transform_messages
from autogen.agentchat.contrib.capabilities.transforms import MessageHistoryLimiter

def create_research_agent(llm_config):

    role = """You are a Research Agent specializing in factual, accurate information.
            Your only job is to research the given topic and return well-structured facts.

            Determine complexity:
            - Simple   → write 5-7  facts
            - Moderate → write 8-11 facts
            - Complex  → write 12-15 facts

            [FACT 1] Your fact here.
            [FACT 2] Your fact here.
            ...

            CRITICAL REQUIREMENT: It is mandatory to put EXACTLY this phrase at the very end of your response:
            RESEARCH COMPLETE
        """


    agent = autogen.AssistantAgent(
        name="ResearchAgent",
        system_message=role,
        llm_config=llm_config,
        max_consecutive_auto_reply=1,
    )

    memory = transform_messages.TransformMessages(
        transforms=[MessageHistoryLimiter(max_messages=10)]
    )
    memory.add_to_agent(agent)

    return agent
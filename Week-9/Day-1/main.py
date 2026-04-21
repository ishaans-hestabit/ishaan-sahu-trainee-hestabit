import os
import autogen
from dotenv import load_dotenv
from agents.research_agent import create_research_agent
from agents.summarizer_agent import create_summarizer_agent
from agents.answer_agent import create_answer_agent


def get_llm_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(current_dir, "..", ".env")
    load_dotenv(dotenv_path=env_path)
    return {
        "config_list": [
            {
                "model": "llama-3.3-70b-versatile",
                "base_url": "https://api.groq.com/openai/v1",
                "api_key": os.environ.get("GROQ_API_KEY"),
                "api_type": "openai",
                "price": [0, 0],
            }
        ],
        "temperature": 0.3,
        "cache_seed": None,
    }


def pick_next_speaker(last_speaker, groupchat):
    if last_speaker.name == "User":
        return groupchat.agents[1]
    if last_speaker.name == "ResearchAgent":
        return groupchat.agents[2]
    if last_speaker.name == "SummarizerAgent":
        return groupchat.agents[3]
    return None


def build_system(llm_config):
    research_agent   = create_research_agent(llm_config)
    summarizer_agent = create_summarizer_agent(llm_config)
    answer_agent     = create_answer_agent(llm_config)

    user = autogen.UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
        code_execution_config=False,
    )

    groupchat = autogen.GroupChat(
        agents=[user, research_agent, summarizer_agent, answer_agent],
        messages=[],
        max_round=8,
        speaker_selection_method=pick_next_speaker,
    )

    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config,
        is_termination_msg=lambda msg: "ANSWER COMPLETE" in msg.get("content", ""),
    )

    return user, manager, groupchat


if __name__ == "__main__":
    llm_config = get_llm_config()
    user, manager, groupchat = build_system(llm_config)

    print("=" * 50)
    print("  Multi-Agent Chain  |  Day 1")
    print("  Type 'exit' to quit.")
    print("=" * 50)

    while True:
        query = input("\nYou: ").strip()
        if not query:
            continue
        if query.lower() == "exit":
            print("Goodbye.")
            break

        groupchat.messages.clear()
        user.initiate_chat(manager, message=query, clear_history=Fale)
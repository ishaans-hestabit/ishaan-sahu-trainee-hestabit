import os
import autogen
from autogen.coding import LocalCommandLineCodeExecutor
from nexus_ai.config import WORKSPACE_DIR, SCRATCH_DIR


def get_code_agent(llm_config):
    os.makedirs(SCRATCH_DIR, exist_ok=True)

    executor = LocalCommandLineCodeExecutor(timeout=60, work_dir=SCRATCH_DIR)

    code_writer = autogen.AssistantAgent(
        name="CodeWriter",
        system_message=f"""You are a Python coding agent.
                Your ONLY output mechanism is a single Python code block.

                RULES:
                1. Always write exactly ONE ```python ... ``` code block per message.
                2. Always use print() to show your code output and results directly.
                3. Do NOT create or save files unless the user explicitly asks to save/create a file.
                4. For "write a program" or "give me code" tasks: just write the code and print() the output.
                5. Only when explicitly asked to save: save to {WORKSPACE_DIR}/<filename>
                6. If a package is missing, install it with subprocess.
                7. If your code fails, fix it and resend.
                8. Do NOT say TERMINATE in the same message as code.
                After seeing execution output, summarize briefly and end with TERMINATE.""",
        llm_config=llm_config,
    )

    code_executor = autogen.UserProxyAgent(
        name="CodeExecutor",
        human_input_mode="NEVER",
        code_execution_config={"executor": executor},
        is_termination_msg=lambda msg: "TERMINATE" in (msg.get("content") or ""),
    )

    return code_writer, code_executor

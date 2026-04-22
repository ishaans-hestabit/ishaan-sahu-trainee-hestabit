import os
import autogen
from autogen.coding import LocalCommandLineCodeExecutor

PROJECT_DIR = os.path.abspath(os.curdir)
SCRATCH_DIR = os.path.join(PROJECT_DIR, ".autogen_scratch")

def get_code_agent(llm_config):
    os.makedirs(SCRATCH_DIR, exist_ok=True)

    executor = LocalCommandLineCodeExecutor(
        timeout=60,
        work_dir=SCRATCH_DIR,  # tmp_code_* files go here instead of project root
    )

    code_writer = autogen.AssistantAgent(
        name="CodeWriter",
        system_message=f"""You are a Python coding agent.
            Your ONLY output mechanism is a single Python code block.

            ABSOLUTE RULES:
            1. You must ALWAYS write exactly ONE ```python ... ``` code block per message.
            2. NEVER output raw HTML, CSS, JS, JSON, YAML, or any non-Python code block directly.
            3. If the task needs multiple files (e.g. HTML + CSS + JS), write ONE Python script
            that creates ALL those files using open() and write().
            4. Always use print() to confirm what was created.
            5. When saving files the user asked for, always write them to: {PROJECT_DIR}/<filename>
            Use absolute paths e.g. open(r"{PROJECT_DIR}/index.html", "w")
            6. If a package is missing, install it first:
    ```python
            import subprocess
            subprocess.check_call(["pip", "install", "package_name"])
    ```
            7. If your code fails, read the error, fix it, and send corrected code.
            8. Do NOT say TERMINATE in the same message as code.
            After seeing execution output, summarize briefly and end with TERMINATE.

            Example for multi-file task:
    ```python
            # Write HTML file
            with open("index.html", "w") as f:
                f.write(\"\"\"<!DOCTYPE html>...\"\"\")

            # Write CSS file
            with open("style.css", "w") as f:
                f.write(\"\"\"body {{ margin: 0; }}\"\"\")

            # Write JS file
            with open("script.js", "w") as f:
                f.write(\"\"\"console.log('ready');\"\"\")

            print("Files created: index.html, style.css, script.js")
    ```
    """,
        llm_config=llm_config,
    )

    code_executor = autogen.UserProxyAgent(
        name="CodeExecutor",
        human_input_mode="NEVER",
        code_execution_config={"executor": executor},
       
        is_termination_msg=lambda msg: "TERMINATE" in (msg.get("content") or ""),
    )

    return code_writer, code_executor
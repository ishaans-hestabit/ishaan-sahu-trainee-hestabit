import csv
import os
from typing import Annotated
import autogen
from nexus_ai.config import WORKSPACE_DIR

MAX_FILE_SIZE = 1_000_000


def get_file_agent(llm_config):
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    assistant = autogen.AssistantAgent(
        name="FileAgent",
        system_message=f"""You are a File Agent with tools to read and write files.
            Use read_csv for CSV files, read_file for text files, write_file to save.
            All files are in: {WORKSPACE_DIR}/
            Just pass the filename (e.g. "sales.csv"), not a full path.
            Show the COMPLETE result from tools. Do NOT summarize.
            End your final message with TERMINATE.""",
        llm_config=llm_config,
    )

    user_proxy = autogen.UserProxyAgent(
        name="FileProxy",
        human_input_mode="NEVER",
        code_execution_config=False,
        is_termination_msg=lambda msg: "TERMINATE" in (msg.get("content") or ""),
    )

    def _resolve_path(filepath: str) -> str:

        candidate = os.path.join(WORKSPACE_DIR, os.path.basename(filepath))
        if os.path.exists(candidate):
            return candidate
        return filepath  

    def read_file(filepath: Annotated[str, "Filename or path to the text file"]) -> str:
        resolved = _resolve_path(filepath)
        try:
            if os.path.getsize(resolved) > MAX_FILE_SIZE:
                return f"Error: File too large. Limit is {MAX_FILE_SIZE} bytes."
            with open(resolved, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return f"Error: File '{filepath}' not found in workspace or at given path."
        except Exception as e:
            return f"Error: {e}"

    def write_file(
            filepath: Annotated[str, "Filename to save inside workspace"],
            content: Annotated[str, "Content to write"]) -> str:
        
        filename = os.path.basename(filepath)
        safe_path = os.path.join(WORKSPACE_DIR, filename)
        try:
            with open(safe_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Written to {safe_path}"
        except Exception as e:
            return f"Error: {e}"

    def read_csv(filepath: Annotated[str, "Filename or path to the CSV file"]) -> str:
        resolved = _resolve_path(filepath)
        try:
            if os.path.getsize(resolved) > MAX_FILE_SIZE:
                return "Error: File too large."
            rows = []
            with open(resolved, "r", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    rows.append(dict(row))
            if not rows:
                return "CSV has no data rows."
            columns = list(rows[0].keys())
            col_widths = {
                col: max(len(col), max(len(str(row[col])) for row in rows))
                for col in columns
            }
            header = " | ".join(col.ljust(col_widths[col]) for col in columns)
            separator = "-+-".join("-" * col_widths[col] for col in columns)
            lines = [f"Total rows: {len(rows)}", f"Columns: {', '.join(columns)}", "", header, separator]
            for row in rows:
                line = " | ".join(str(row[col]).ljust(col_widths[col]) for col in columns)
                lines.append(line)
            return "\n".join(lines)
        except FileNotFoundError:
            return f"Error: File '{filepath}' not found in workspace or at given path."
        except Exception as e:
            return f"Error: {e}"

    assistant.register_for_llm(name="read_file", description="Reads a text/JSON/HTML file and returns its content.")(read_file)
    assistant.register_for_llm(name="write_file", description="Writes content to a file in the workspace.")(write_file)
    assistant.register_for_llm(name="read_csv", description="Reads a CSV file and returns it as a formatted table.")(read_csv)

    user_proxy.register_for_execution(name="read_file")(read_file)
    user_proxy.register_for_execution(name="write_file")(write_file)
    user_proxy.register_for_execution(name="read_csv")(read_csv)

    return assistant, user_proxy
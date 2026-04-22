import csv
import os
from typing import Annotated
import autogen

MAX_FILE_SIZE_BYTES = 1_000_000 
FILES_DIR = os.path.join(os.path.abspath(os.curdir), "files")


def get_file_agent(llm_config):
    os.makedirs(FILES_DIR, exist_ok=True)

    assistant = autogen.AssistantAgent(
        name="FileAgent",
        system_message=f"""You are a File Agent.
            You have tools to read and write files.
            Use read_csv to read CSV files.
            Use read_file for plain text files.
            Use write_file to save content to disk.
            IMPORTANT: All files are saved into: {FILES_DIR}/
            Just pass the filename (e.g. "report.txt"), NOT a full path.
            If a file is not found, say so clearly.
            After completing the task, print the COMPLETE result exactly as returned by the tool.
            Do NOT summarize or paraphrase tool output — show it fully.
            End your final message with TERMINATE.""",
        llm_config=llm_config,
    )

    user_proxy = autogen.UserProxyAgent(
        name="FileProxy",
        human_input_mode="NEVER",
        code_execution_config=False,
        
        is_termination_msg=lambda msg: "TERMINATE" in (msg.get("content") or ""),
    )

    def read_file( filepath: Annotated[str, "Path to the plain text file to read"]) -> str:

        try:
            size = os.path.getsize(filepath)
            if size > MAX_FILE_SIZE_BYTES:
                return f"Error: File too large ({size} bytes). Limit is {MAX_FILE_SIZE_BYTES} bytes."
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return f"Error: File '{filepath}' not found."
        except Exception as e:
            return f"Error: {str(e)}"

    def write_file(
                filepath: Annotated[str, "Filename or path — file will be saved inside the files/ directory"],
                content: Annotated[str, "Text content to write into the file"]) -> str:

       
        filename = os.path.basename(filepath)
        safe_path = os.path.join(FILES_DIR, filename)
        try:
            os.makedirs(FILES_DIR, exist_ok=True)
            with open(safe_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully written to {safe_path}"
        except Exception as e:
            return f"Error: {str(e)}"

    def read_csv( filepath: Annotated[str, "Path to the CSV file to read"] ) -> str:
        
        try:
            if os.path.getsize(filepath) > MAX_FILE_SIZE_BYTES:
                return f"Error: File too large. Limit is {MAX_FILE_SIZE_BYTES} bytes."

            rows = []
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(dict(row))

            if not rows:
                return "CSV file has no data rows."

            columns = list(rows[0].keys())

            
            col_widths = {
                col: max(len(col), max(len(str(row[col])) for row in rows))
                for col in columns
            }

         
            header = " | ".join(col.ljust(col_widths[col]) for col in columns)
            separator = "-+-".join("-" * col_widths[col] for col in columns)

            lines = [
                f"Total rows: {len(rows)}",
                f"Columns: {', '.join(columns)}",
                "",
                header,
                separator,
            ]

            for row in rows:
                line = " | ".join(str(row[col]).ljust(col_widths[col]) for col in columns)
                lines.append(line)

            return "\n".join(lines)

        except FileNotFoundError:
            return f"Error: File '{filepath}' not found."
        except Exception as e:
            return f"Error: {str(e)}"

  
    assistant.register_for_llm( name="read_file", description="Reads a plain text file and returns its content. Input: file path.")(read_file)

    assistant.register_for_llm( name="write_file", description="Writes text content to a file on disk. Inputs: file path and content string." )(write_file)

    assistant.register_for_llm( name="read_csv", description="Reads a CSV file and returns all rows as a formatted table. Input: file path.")(read_csv)

   
    user_proxy.register_for_execution(name = "read_file")(read_file)
    user_proxy.register_for_execution(name = "write_file")(write_file)
    user_proxy.register_for_execution(name = "read_csv")(read_csv)

    return assistant, user_proxy
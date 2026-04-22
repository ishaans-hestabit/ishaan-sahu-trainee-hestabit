import sqlite3
from typing import Annotated
import autogen

DB_PATH = "day3_database.db"


def get_db_agent(llm_config):
    assistant = autogen.AssistantAgent(
        name="DBAgent",
        system_message="""You are a Database Agent.
            You have tools to work with a SQLite database.

            IMPORTANT — before doing anything, think about what the task requires:
            - If the task is ONLY to query/fetch/read existing data: call query_db directly.
            Do NOT create tables or insert data unless the task explicitly asks for it.
            - If the task asks to CREATE a table: use create_table first.
            - If the task asks to INSERT data: use insert_data.
            - If the task asks to query after inserting: use query_db last.

            Never insert sample/dummy data unless the user explicitly asked for it.
            Never recreate a table that already exists with data in it.

            Your final message MUST contain the complete query output.
            Copy every row from query_db exactly as returned.
            Do NOT summarize or skip rows.
            End your final message with TERMINATE.""",
        llm_config=llm_config,
    )

   
    user_proxy = autogen.UserProxyAgent(
        name="DBProxy",
        human_input_mode="NEVER",
        code_execution_config=False,
        is_termination_msg=lambda msg: "TERMINATE" in (msg.get("content") or ""),
    )

    def create_table(sql: Annotated[str, "A CREATE TABLE IF NOT EXISTS SQL statement"]) -> str:
        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute(sql)
                conn.commit()
            return "Table created successfully."
        except Exception as e:
            return f"Error: {str(e)}"

    def insert_data(sql: Annotated[str, "An INSERT INTO SQL statement"]) -> str:
        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute(sql)
                conn.commit()
            return "Data inserted successfully."
        except Exception as e:
            return f"Error: {str(e)}"

    def query_db(sql: Annotated[str, "A SELECT SQL statement"]) -> str:
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.execute(sql)
                rows = cursor.fetchall()
                columns = [d[0] for d in cursor.description]

            if not rows:
                return "Query returned 0 rows."

          
            col_widths = {
                col: max(len(col), max(len(str(row[i])) for row in rows))
                for i, col in enumerate(columns)
            }

            header    = " | ".join(col.ljust(col_widths[col]) for col in columns)
            separator = "-+-".join("-" * col_widths[col] for col in columns)
            lines     = [f"Rows returned: {len(rows)}", "", header, separator]

            for row in rows:
                line = " | ".join(str(row[i]).ljust(col_widths[col]) for i, col in enumerate(columns))
                lines.append(line)

            return "\n".join(lines)

        except Exception as e:
            return f"Error: {str(e)}"

    assistant.register_for_llm(name="create_table", description="Creates a table in SQLite. Input: CREATE TABLE IF NOT EXISTS SQL statement.")(create_table)
    assistant.register_for_llm(name="insert_data",  description="Inserts a row into a table. Input: INSERT INTO SQL statement.")(insert_data)
    assistant.register_for_llm(name="query_db",     description="Runs a SELECT query and returns formatted rows. Input: SELECT SQL statement.")(query_db)

    user_proxy.register_for_execution(name="create_table")(create_table)
    user_proxy.register_for_execution(name="insert_data")(insert_data)
    user_proxy.register_for_execution(name="query_db")(query_db)

    return assistant, user_proxy
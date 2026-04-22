import sqlite3
from typing import Annotated
import autogen
from nexus_ai.config import DB_PATH


def get_db_agent(llm_config):
    assistant = autogen.AssistantAgent(
        name="DBAgent",
        system_message="""You are a Database Agent with SQLite tools.
            Before doing anything, think about what the task requires:
            - Query/fetch data: use query_db directly.
            - Create a table: use create_table.
            - Insert data: use insert_data.
            Never insert sample data unless explicitly asked.
            Your final message MUST contain the complete query output.
            End your final message with TERMINATE.""",
        llm_config=llm_config,
    )

    user_proxy = autogen.UserProxyAgent(
        name="DBProxy",
        human_input_mode="NEVER",
        code_execution_config=False,
        is_termination_msg=lambda msg: "TERMINATE" in (msg.get("content") or ""),
    )

    def create_table(sql: Annotated[str, "CREATE TABLE IF NOT EXISTS SQL statement"]) -> str:
        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute(sql)
                conn.commit()
            return "Table created successfully."
        except Exception as e:
            return f"Error: {e}"

    def insert_data(sql: Annotated[str, "INSERT INTO SQL statement"]) -> str:
        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute(sql)
                conn.commit()
            return "Data inserted successfully."
        except Exception as e:
            return f"Error: {e}"

    def query_db(sql: Annotated[str, "SELECT SQL statement"]) -> str:
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
            header = " | ".join(col.ljust(col_widths[col]) for col in columns)
            separator = "-+-".join("-" * col_widths[col] for col in columns)
            lines = [f"Rows returned: {len(rows)}", "", header, separator]
            for row in rows:
                line = " | ".join(str(row[i]).ljust(col_widths[col]) for i, col in enumerate(columns))
                lines.append(line)
            return "\n".join(lines)
        except Exception as e:
            return f"Error: {e}"

    assistant.register_for_llm(name="create_table", description="Creates a SQLite table.")(create_table)
    assistant.register_for_llm(name="insert_data", description="Inserts data into a table.")(insert_data)
    assistant.register_for_llm(name="query_db", description="Runs a SELECT query.")(query_db)

    user_proxy.register_for_execution(name="create_table")(create_table)
    user_proxy.register_for_execution(name="insert_data")(insert_data)
    user_proxy.register_for_execution(name="query_db")(query_db)

    return assistant, user_proxy

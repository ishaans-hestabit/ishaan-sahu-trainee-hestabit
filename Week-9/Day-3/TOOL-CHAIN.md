# TOOL-CHAIN.md

## Two Approaches Used in Day 3

Approach 1 — Tool Use (DB Agent, File Agent)
  You define specific Python functions.
  Register them with the agent.
  The LLM calls them by name with arguments.
  The UserProxy physically runs them.
  Best for: controlled, specific operations.

Approach 2 — Code Executor (Code Agent)
  The LLM writes Python code in a code block.
  LocalCommandLineCodeExecutor extracts the code.
  Runs it in a real subprocess on your machine.
  Sends back the printed output.
  Best for: open-ended computation and data analysis.

## Tool Use Registration Pattern

assistant.register_for_llm(name="tool", description="what it does")(function)
user_proxy.register_for_execution(name="tool")(function)

register_for_llm  -> tells the LLM the tool exists
register_for_execution -> tells the proxy to actually run it

## Code Executor Pattern

executor = LocalCommandLineCodeExecutor(timeout=30, work_dir=folder)
code_executor_agent = UserProxyAgent(code_execution_config={"executor": executor})

The LLM writes:
```python
print("hello")
```
The executor extracts this block, runs it, returns the output.

## The Three Agents

File Agent (Tool Use)
  read_file  — reads any text file
  write_file — writes content to a file
  read_csv   — reads CSV and returns structured rows

DB Agent (Tool Use)
  create_table — CREATE TABLE SQL
  insert_data  — INSERT INTO SQL
  query_db     — SELECT SQL, returns rows

Code Agent (Code Executor)
  LLM writes Python code blocks
  Executor runs them in a subprocess
  Output sent back to LLM

## Install

pip install "ag2[groq]"

csv, sqlite3, tempfile are all built into Python.
No extra packages needed.
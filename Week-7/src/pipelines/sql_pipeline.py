import os
import re
import sys
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.schema_loader      import get_schema
from generator.sql_generator  import generate_sql, summarize_result

DB_PATH = Path("data/enterprise.db")

BLOCKED_KEYWORDS = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "TRUNCATE", "CREATE"]


def validate_sql(sql: str, db_path: str) -> dict:
    if not sql.strip():
        return {"valid": False, "error": "SQL query is empty."}

    sql_upper = sql.upper()

    for keyword in BLOCKED_KEYWORDS:
        if re.search(r'\b' + keyword + r'\b', sql_upper):
            return {"valid": False, "error": f"Blocked keyword '{keyword}' found. Only SELECT queries are allowed"}

    first_word = sql_upper.strip().split()[0]
    if first_word != "SELECT":
        return {"valid": False, "error": f"Query must start with SELECT. Got: '{first_word}'"}

    try:
        conn = sqlite3.connect(str(db_path))
        conn.execute(f"EXPLAIN {sql}")
        conn.close()
    except sqlite3.OperationalError as e:
        return {"valid": False, "error": f"SQL syntax error: {e}"}

    return {"valid": True, "error": None}


def execute_sql(sql: str, db_path: str) -> dict:
    try:
        conn   = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        cursor.execute(sql)

        rows    = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        conn.close()

        return {"success": True, "columns": columns, "rows": rows, "error": None}

    except Exception as e:
        return {"success": False, "columns": [], "rows": [], "error": str(e)}


def answer_question(question: str, db_path: str = DB_PATH) -> dict:

    print(f"\n{'='*55}")
    print(f"  Question : {question}")
    print(f"  Database : {db_path}")
    print(f"{'='*55}")

    print("\nLoading database schema...")
    try:
        schema = get_schema(str(db_path))
        print(f"  OK — schema loaded ({len(schema)} chars)")
    except FileNotFoundError as e:
        print(f"  FAILED — {e}")
        return {"success": False, "error": str(e), "question": question, "sql": "", "answer": ""}

    print("Asking Grok to write SQL...")
    gen = generate_sql(question, schema)
    if not gen["success"]:
        print(f"  FAILED — {gen['error']}")
        return {"success": False, "error": gen["error"], "question": question, "sql": "", "answer": ""}
    print(f"  OK — {gen['sql'][:70]}...")
    if gen["explanation"]:
        print(f"       ({gen['explanation']})")

    
    print("Validating SQL (safety + syntax)...")
    val = validate_sql(gen["sql"], str(db_path))
    if not val["valid"]:
        print(f"  FAILED — {val['error']}")
        return {"success": False, "error": val["error"], "question": question, "sql": gen["sql"], "answer": ""}
    print("  OK — safe to execute ✅")

    
    print("Executing SQL on database...")
    exe = execute_sql(gen["sql"], str(db_path))
    if not exe["success"]:
        print(f"  FAILED — {exe['error']}")
        return {"success": False, "error": exe["error"], "question": question, "sql": gen["sql"], "answer": ""}
    print(f"  OK — {exe['row_count'] if 'row_count' in exe else len(exe['rows'])} rows returned")

    
    print("Asking Grok to summarize results...")
    answer = summarize_result(question, gen["sql"], exe["columns"], exe["rows"])
    print("  OK")

    
    print(f"\n{'─'*55}")
    print(f"  SQL    : {gen['sql']}")
    print(f"{'─'*55}")
    print(f"  ANSWER : {answer}")
    print(f"{'─'*55}\n")

    return {
        "success" : True,
        "error"   : None,
        "question": question,
        "sql"     : gen["sql"],
        "columns" : exe["columns"],
        "rows"    : exe["rows"],
        "answer"  : answer,
    }

def create_sample_db(db_path: Path = DB_PATH):
    """Creates a realistic enterprise.db for testing."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    conn.executescript("""
        DROP TABLE IF EXISTS sales;
        DROP TABLE IF EXISTS employees;
        DROP TABLE IF EXISTS products;

        CREATE TABLE employees (
            id         INTEGER PRIMARY KEY,
            name       TEXT    NOT NULL,
            department TEXT    NOT NULL,
            salary     REAL    NOT NULL,
            hire_date  TEXT    NOT NULL
        );

        CREATE TABLE products (
            id        INTEGER PRIMARY KEY,
            name      TEXT    NOT NULL,
            category  TEXT    NOT NULL,
            price     REAL    NOT NULL,
            stock_qty INTEGER NOT NULL
        );

        CREATE TABLE sales (
            id           INTEGER PRIMARY KEY,
            product_id   INTEGER NOT NULL,
            employee_id  INTEGER NOT NULL,
            quantity     INTEGER NOT NULL,
            total_amount REAL    NOT NULL,
            sale_date    TEXT    NOT NULL,
            region       TEXT    NOT NULL
        );
    """)

    conn.executemany("INSERT INTO employees VALUES (?,?,?,?,?)", [
        (1,  "Alice Johnson",  "Engineering", 95000,  "2020-03-15"),
        (2,  "Bob Smith",      "Marketing",   72000,  "2019-07-22"),
        (3,  "Charlie Brown",  "Engineering", 88000,  "2021-01-10"),
        (4,  "Diana Prince",   "HR",          68000,  "2018-05-30"),
        (5,  "Ethan Hunt",     "Engineering", 102000, "2017-11-01"),
        (6,  "Fiona Green",    "Marketing",   75000,  "2022-02-14"),
        (7,  "George Miller",  "Finance",     85000,  "2020-08-19"),
        (8,  "Hannah Lee",     "HR",          62000,  "2023-03-01"),
        (9,  "Ivan Drago",     "Finance",     91000,  "2019-12-15"),
        (10, "Julia Roberts",  "Marketing",   69000,  "2021-06-05"),
    ])

    conn.executemany("INSERT INTO products VALUES (?,?,?,?,?)", [
        (1, "Cloud Analytics Suite",  "Software",  4999.99, 500),
        (2, "DataSync Pro",           "Software",  2499.99, 300),
        (3, "SecureVault Enterprise", "Software",  1999.99, 400),
        (4, "ProServer 4000",         "Hardware",  8999.99, 80),
        (5, "SmartRouter X9",         "Hardware",  1299.99, 150),
        (6, "Consulting Hours Pack",  "Services",  5000.00, 999),
        (7, "Annual Support",         "Services",  2400.00, 999),
    ])

    conn.executemany("INSERT INTO sales VALUES (?,?,?,?,?,?,?)", [
        (1,  1, 2,  2,  9999.98,  "2024-01-15", "North"),
        (2,  4, 6,  1,  8999.99,  "2024-01-20", "South"),
        (3,  2, 10, 3,  7499.97,  "2024-02-03", "East"),
        (4,  6, 2,  5,  25000.00, "2024-02-10", "North"),
        (5,  3, 6,  2,  3999.98,  "2024-02-18", "West"),
        (6,  1, 10, 1,  4999.99,  "2024-03-15", "North"),
        (7,  7, 6,  10, 24000.00, "2024-03-22", "East"),
        (8,  5, 10, 5,  6499.95,  "2024-04-01", "West"),
        (9,  2, 2,  2,  4999.98,  "2024-04-10", "North"),
        (10, 4, 6,  2,  17999.98, "2024-04-25", "South"),
        (11, 6, 10, 3,  15000.00, "2024-05-05", "East"),
        (12, 1, 2,  1,  4999.99,  "2024-05-12", "North"),
        (13, 3, 6,  4,  7999.96,  "2024-06-01", "West"),
        (14, 2, 2,  1,  2499.99,  "2024-08-14", "South"),
        (15, 5, 6,  10, 12999.90, "2024-09-01", "North"),
    ])

    conn.commit()
    conn.close()
    print(f"Sample database created: {db_path}")
    print("   Tables: employees (10 rows), products (7 rows), sales (15 rows)")
    print(f"\n   Now run: python pipelines/sql_pipeline.py")


if __name__ == "__main__":
    
    if "--setup" in sys.argv:
        create_sample_db()
        sys.exit()

    if len(sys.argv) > 1:
        answer_question(" ".join(sys.argv[1:]))
        sys.exit()

    demo_questions = [
        "What is the average salary by department?",           
        "Show total sales amount by region",                   
        "Who are the top 3 highest paid employees?",           
        "Which product category generated the most revenue?",  
        "How many employees were hired each year?",            
    ]

    for question in demo_questions:
        answer_question(question)
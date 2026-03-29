import sqlite3
from pathlib import Path


def get_schema(db_path: str) -> str:
    if not Path(db_path).exists():
        raise FileNotFoundError(f"Database not found: '{db_path}'\nRun: python pipelines/sql_pipeline.py --setup")

    conn   = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [row[0] for row in cursor.fetchall()]

    if not tables:
        conn.close()
        return "No tables found in database."

    lines = [f"DATABASE: {Path(db_path).name}", f"TABLES: {', '.join(tables)}", ""]

    for table in tables:
        lines.append(f"TABLE: {table}")

        cursor.execute(f"PRAGMA table_info('{table}');")
        columns = cursor.fetchall()

        for col in columns:
            pk_tag   = " [PK]"   if col[5] else ""
            null_tag = " NOT NULL" if col[3] else ""
            lines.append(f"  - {col[1]} {col[2]}{pk_tag}{null_tag}")

        cursor.execute(f"SELECT * FROM '{table}' LIMIT 3;")
        sample_rows = cursor.fetchall()
        col_names   = [col[1] for col in columns]

        if sample_rows:
            lines.append(f"  Sample data ({' | '.join(col_names)}):")
            for row in sample_rows:
                lines.append("    " + " | ".join(str(v) for v in row))

        lines.append("")  

    conn.close()
    return "\n".join(lines)
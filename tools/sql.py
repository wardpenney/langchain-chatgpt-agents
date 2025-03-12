import sqlite3
from langchain.tools import Tool

conn = sqlite3.connect("db.sqlite")

def list_tables():
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    rows = cursor.fetchall()
    return "\n".join([row[0] for row in rows if row[0] is not None])

def run_sqlite_query(query):
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        return f"The following error occurred: {str(e)}"

run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Use this to run a query against the database",
    func=run_sqlite_query,
)

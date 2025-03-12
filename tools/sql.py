import sqlite3
from pydantic.v1 import BaseModel
from typing import List
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

class RunQueryArgsSchema(BaseModel):
    query: str

run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Use this to run a query against the database",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema
)

class DescribeTablesArgsSchema(BaseModel):
    table_names: List[str]

def describe_tables(table_names):
    cursor = conn.cursor()
    tables = ",".join("'" + table + "'" for table in table_names)
    rows = cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name IN ({tables});")
    return "\n".join(f"{row[0]}" for row in rows if row[0] is not None)

describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Use this to describe the given tables in the database",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema
)

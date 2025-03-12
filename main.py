from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv
from tools.sql import run_query_tool, list_tables, describe_tables_tool
from tools.report import write_report_tool

load_dotenv()

chat = ChatOpenAI()

tables = list_tables()
prompt = ChatPromptTemplate.from_messages(
  messages=[
    SystemMessage(content=(
        f"You are a helpful assistant that can run SQL queries. The following tables are available: {tables}"
        f"You can use the `describe_tables` tool to describe the tables in the database.\n"
        f"Do not make any assumptions about the database. Only use the tools provided to you.\n"
        f"If you need to describe a table, use the `describe_tables` tool.\n"
        f"If you need to run a query, use the `run_query` tool.\n"
        f"If you need to list the tables, use the `list_tables` tool.\n"
      ),
    ),
    HumanMessagePromptTemplate.from_template("{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
  ]
)

tools = [
  run_query_tool,
  describe_tables_tool,
  write_report_tool
]

agent = OpenAIFunctionsAgent(
  llm=chat,
  tools=tools,
  prompt=prompt,
)

agent_executor = AgentExecutor(
  agent=agent,
  tools=tools,
  verbose=True,
)

agent_executor("Summarize the top 5 most popular products in the database. Write the report to a file called 'report.html'.")

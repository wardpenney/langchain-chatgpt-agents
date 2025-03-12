from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables, describe_tables_tool
from tools.report import write_report_tool
from tools.handlers.chat_model_start_handler import ChatModelStartHandler

load_dotenv()

handler = ChatModelStartHandler()
chat = ChatOpenAI(
  callbacks=[handler]
)

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
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
  ]
)

memory = ConversationBufferMemory(
  memory_key="chat_history",
  return_messages=True
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
  # verbose=True,
  memory=memory
)

agent_executor(
  "How many orders are there in the database? Write the results to a html report with the extension .html."
)

agent_executor(
  "Repeat the exact same process for users."
)

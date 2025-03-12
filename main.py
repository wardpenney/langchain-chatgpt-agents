from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv
from tools.sql import run_query_tool, list_tables


load_dotenv()

chat = ChatOpenAI()

tables = list_tables()
prompt = ChatPromptTemplate.from_messages(
  messages=[
    SystemMessage(content=f"You are a helpful assistant that can run SQL queries. The following tables are available: {tables}"),
    HumanMessagePromptTemplate.from_template("{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
  ]
)

tools = [run_query_tool]

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

agent_executor("How many users have a shipping address in the database?")

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()
LLM = ChatOpenAI(model="gpt-4o")
server_params = StdioServerParameters(
    command="python",
    args=["mcp_servers/first_mcp_server.py"]
)


async def ask_react_agent(message: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session=session)
            AGENT = create_react_agent(LLM, tools=tools)
            response = await AGENT.ainvoke({"messages": message})
            for m in response['messages']:
                m.pretty_print()

if __name__ == "__main__":
    asyncio.run( ask_react_agent(message="what tools do you have"))


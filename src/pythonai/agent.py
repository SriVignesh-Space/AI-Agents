from dotenv import load_dotenv
import os

load_dotenv()

import requests
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage

model = ChatOllama(model="nemotron-3-nano:30b-cloud",
    temperature=0)

@tool('get_weather', description="get the latest temperature details for a given city")
def get_weather(city:str):
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    return response.json()


agents = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="you are the comedian weather assistant. now tell the current weather status of the given city"
)

messages= [
        HumanMessage(content="what is the current temperature of chennai?")
    ]

response = agents.invoke({
    "messages": [
        HumanMessage(content="what is the current temperature of chennai?")
    ]
}, )

print(response['messages'][-1].content)
for msg in response["messages"]:
    print("TYPE:", type(msg).__name__)
    print("CONTENT:", msg.content)

    if hasattr(msg, "tool_calls"):
        print("TOOL CALLS:", msg.tool_calls)
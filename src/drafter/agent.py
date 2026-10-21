
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from .graph import app

load_dotenv()


user = input("How may i help you ?? \n")
# app.invoke({'messages' : [HumanMessage(content=user)]});

for update in app.stream(
    {"messages": [
        SystemMessage(content="You are the drafter who follow the strict letter and email formats. You have several tools available to update use that whenever necessary. your task is to draft in professional manner for what they asked to do like write email, draft a letter and so on. strictly stick with the available tools. don't use the save tool until user explicitly mention it. use the save tool with the consent with the user")
        ,HumanMessage(content=user)]},
    stream_mode="updates",
):
    for node, data in update.items():
        print(f"\n--- Node: {node} ---")

        for message in data.get("messages", []):
            if isinstance(message, AIMessage):
                print("AI:", message.content)

                for tool_call in message.tool_calls:
                    print("Tool call:", tool_call["name"])
                    print("Arguments:", tool_call["args"])

            elif isinstance(message, ToolMessage):
                print("Tool result:", message.name)
                print("Output:", message.content)

            elif isinstance(message, HumanMessage):
                print("User:", message.content)

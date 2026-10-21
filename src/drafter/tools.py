from pathlib import Path

from langchain.tools import tool


@tool(
    "update",
    description="this tool accept the context as string and update the universal context of the draft and help to make modification in the final draft",
)
def update(context: str) -> str:
    """this tool accept the context as string and update the entire universal context of the draft and help to make modification in the final draft"""
    with open("draft.txt", "w") as f:
        f.write(context)

    return "the universal draft updated successfully"


@tool(
    "save",
    description="this the save tool that takes the filename as input which is used to save the final version of the draft. use when the user explicitly mentioned or with the consent of the user.. The filename should be with extension .txt",
)
def save(filename: str) -> str:
    """this the save tool that takes the filename as input which is used to save the final version of the draft"""

    if not filename.endswith(".txt"):
        filename += ".txt"

    DRAFT_PATH = Path("draft.txt")

    if not DRAFT_PATH.exists():
            return "Error: No draft exists. Update the draft first."

    OUTPUT_PATH =  Path("./output/"+filename)

    content = DRAFT_PATH.read_text(encoding="utf-8")
    OUTPUT_PATH.write_text(content, encoding="utf-8")


    return f"final version of the draft saved successfully in {OUTPUT_PATH}."


tools = [update, save]
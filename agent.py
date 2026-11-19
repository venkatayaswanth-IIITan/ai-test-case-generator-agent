
from langchain_ollama import ChatOllama
from prompts import SYSTEM_PROMPT


def create_agent():

    llm = ChatOllama(
        model="llama3.2:3b",
        temperature=0.2
    )

    return llm


def run_agent(requirement):

    llm = create_agent()

    response = llm.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", f"Analyze this requirement:\n{requirement}")
    ])

    return response.content

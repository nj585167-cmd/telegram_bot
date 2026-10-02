import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from tools import *


# Load environment variables
load_dotenv()


# Get Gemini API key from environment
GEMINI_API_KEY = os.getenv("gemini_key")



# Initialize Gemini
llm_gemini = init_chat_model(
    "google_genai:gemini-3.1-flash-lite",
    api_key=GEMINI_API_KEY
)

info_agent = create_agent(
    model=llm_gemini,
    tools=[get_cricket_score,get_football_score,get_live_value],
    checkpointer=InMemorySaver(),
    system_prompt="""
    YOu are a helpful assistant. who uses relevant tools based on user info
    When user asks about cricket score -> use get_crciket _score
    When user asks about get_live_value -> use get_live_value
    When user asks about football score -> use get_football_score
"""
)
term_plan_agent = create_agent(
    model=llm_gemini,
    tools=[term_plan_eligibility],
    checkpointer=InMemorySaver(),
    system_prompt="""
    YOu are a helpful assistant. who uses relevant tools based on user info
    When user asks about term plan eligibility -> use term_plan_eligibility
"""
)

# Create agent
agent = create_agent(
    model=llm_gemini,
    tools=[as_info_agent,as_term_plan_agent],
    checkpointer=InMemorySaver(),
    system_prompt="""
    YOu are a helpful assistant. who uses relevant tools based on user info
    When user asks about cricket score -> use get_crciket _score
    When user asks about football score -> use get_football_score
    when user asks about term plan hlv value ->  use term_plan_eligibilty
"""
)


# Configuration for memory
config = {
    "configurable": {
        "thread_id": "1"
    }
}


# Interactive command line loop
if __name__ == "__main__":

    print("Agent is ready! (Type 'exit' or 'quit' to stop)")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        response = agent.invoke(
            {
                "messages": [
                    ("user", user_input)
                ]
            },
            config
        )

        print(
            f"Agent: {response['messages'][-1].content}"
        )
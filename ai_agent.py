
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from tools import get_cricket_score


gemini_key = os.getenv('gemini_key')
llm_gemini = init_chat_model(
    "google_genai:gemini-3.1-flash-lite",
    api_key='AQ.Ab8RN6LbnhdgsWQVKRjebcj2ygQ6nd9ifQD6dxRnkuaGmO7WYQ'  
)



agent = create_agent(
    model=llm_gemini,
    tools=[get_cricket_score],
    checkpointer=InMemorySaver(),
    system_prompt="""You are a helpful assistant"""
)


# Configuration for memory (required by InMemorySaver)
config = {"configurable": {"thread_id": "1"}}

# Interactive command line loop
if __name__ == "__main__":
    print("Agent is ready! (Type 'exit' or 'quit' to stop)")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        # Run the agent with the user's input
        response = agent.invoke({"messages": [("user", user_input)]}, config)
        
        # Print the latest response from the agent
        print(f"Agent: {response['messages'][-1].content}")
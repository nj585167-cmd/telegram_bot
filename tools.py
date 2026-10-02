def get_cricket_score(country:str)->str:
    """Use this tool when user asks about cricket scores between India and another country"""
    return f"Score between India and {country} is 120-3"


def get_football_score(country:str)->str:
    """use this tool when user asks about football scores between spain and another country"""
    return f"Score between spain and {country} is 4-3"


    import time
from langchain.messages import HumanMessage
from langchain.tools import tool
import yfinance as yf
from datetime import datetime

def get_live_value(symbol):
    """Fetch short live price and % change"""
    try:
        ticker = yf.Ticker(symbol)
        price = ticker.fast_info.last_price
        prev = ticker.fast_info.previous_close
        change = ((price - prev) / prev) * 100
        print(f"\n📈 {symbol.upper()} -> Price: ₹{price:.2f} | Change: {change:+.2f}%\n")
    except Exception:
        print("\n❌ Fetch failed. Valid symbol check karo (e.g. RELIANCE.NS, ^NSEI, ^BSESN)\n")

def as_info_agent (question :str)-> str:
    """ask the question to "info agent" and return about cricket,football and value."""
    r = as_info_agent .invoke({"messages": [HumanMessage(content = question)]})
    return r["message"][-1].content[0]['text']


from langchain.tools import tool

@tool
def term_plan_eligibility(age: int, education: str, income: float) -> str:
    """Check if customer is eligible for a term plan based on age, education, and income."""
    
    if age >= 18 and age <= 60:
        if income >= 300000:
            if education.lower() == "graduate":
                return "You are eligible for term plan."
            else:
                return "Not eligible: Must be a graduate."
        else:
            return "Not eligible: Income below required limit."
    else:
        return "Customer is not eligible due to age criteria."
 
def as_term_plan_agent (question :str)-> str:
    """ask the question to "info agent" and return about term plan eligibility."""
    r = as_term_plan_agent.invoke({"messages": [HumanMessage(content = question)]})
    return r["message"][-1].content[0]['text']


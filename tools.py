def get_cricket_score(country:str)->str:
    """Use this tool when user asks about cricket scores between India and another country"""
    return f"Score between India and {country} is 120-3"


def get_football_score(country:str)->str:
    """use this tool when user asks about football scores between spain and another country"""
    return f"Score between spain and {country} is 4-3"


    import time
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

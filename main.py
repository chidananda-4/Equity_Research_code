openai_key = '***************************************'
seper_key = '****************************************'
tavily_key ="****************************************"
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = openai_key
os.environ["seper_key"] = seper_key
os.environ["TAVILY_API_KEY"] = tavily_key



from crew import analyze_stock



# Test the implementation with a sample stock
if __name__ == "__main__":
    # Example analysis
    ticker = "TATAMOTORS"
    risk_tolerance = "neutral"  # Options: "averse", "neutral", "seeking"

    try:
        result = analyze_stock(ticker, risk_tolerance)
        print("\n" + "="*50)
        print("FINAL ANALYSIS RESULT")
        print("="*50)
        print(result)
    except Exception as e:
        print(f"Error during analysis: {e}")
        print("This might be due to API limitations:")


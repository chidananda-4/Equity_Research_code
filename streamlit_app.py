import streamlit as st
from main import agent_run  
def main():
    st.title("Multi-Agent Stock Analysis and Recommendation")

    st.write("Enter the ticker symbol of the stock to analyze and choose your risk tolerance.")

    ticker = st.text_input("Ticker Symbol", value="TATAMOTORS")
    risk_tolerance = st.selectbox("Risk Tolerance", options=["Risk-Neutral", "Risk-Averse"])

    if st.button("Get Recommendation"):
        # Integrate with your existing system logic here. Example placeholder:
        recommendation = get_stock_recommendation(ticker, risk_tolerance)
        st.write(f"**Recommendation for {ticker} ({risk_tolerance}): {recommendation}**")

def get_stock_recommendation(ticker, risk_tolerance):
    result = agent_run(ticker,risk_tolerance)
    return result

if __name__ == "__main__":
    main()

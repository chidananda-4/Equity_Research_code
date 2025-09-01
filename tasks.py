# Define tasks for each agent with risk tolerance consideration
from crewai import Agent,Task,Crew,Process
from tools import get_stock_data_tool,get_financials_tool,calculate_metrics_tool,get_news_tool,analyze_sentiment_tool,scrape_tool
from agents import valuation_agent,sentiment_agent,fundamental_agent,debate_manager

def create_valuation_task(ticker, risk_tolerance="neutral"):
    risk_prompt = ""
    if risk_tolerance == "averse":
        risk_prompt = "Focus on risk mitigation, volatility concerns, and capital preservation. "
    elif risk_tolerance == "seeking":
        risk_prompt = "Focus on growth potential and higher return opportunities. "
    else:
        risk_prompt = "Balance risk and return considerations. "

    return Task(
        description=f"""
        Analyze the valuation trends of {ticker} stock using the FinancialDataTool.
        {risk_prompt}
        Calculate and consider key metrics including:
        - Cumulative returns
        - Annualized returns
        - Volatility measures
        - Price trends and patterns.
        Use the FinancialDataTool's `calculate_metrics` and `get_stock_data` methods to gather necessary data.

        Provide a BUY or SELL recommendation with detailed justification based on the valuation analysis and the {risk_tolerance} risk tolerance.
        """,
        agent=valuation_agent,
        tools=[calculate_metrics_tool, get_stock_data_tool],  # Use the new tool instances
        expected_output="A detailed valuation analysis with metrics, trend analysis, and a clear BUY/SELL recommendation."
    )

def create_sentiment_task(ticker, risk_tolerance="neutral"):
    risk_prompt = ""
    if risk_tolerance == "averse":
        risk_prompt = "Be particularly cautious about negative news and sentiment. "
    elif risk_tolerance == "seeking":
        risk_prompt = "Focus on positive momentum and growth sentiment. "
    else:
        risk_prompt = "Balance positive and negative sentiment factors. "

    return Task(
        description=f"""
        Analyze news sentiment and market perception for {ticker} using the NewsSentimentTool.
        {risk_prompt}
        Consider:
        - Recent news articles and their tone. Use the NewsSentimentTool's `get_news` method.
        - Analyze sentiment based on the news using the NewsSentimentTool's `analyze_sentiment` method.
        - Analyst rating changes (if available through scraping or other means).
        - Market sentiment indicators.
        - Any significant corporate events or disclosures.

        Provide a BUY or SELL recommendation based on sentiment analysis and the {risk_tolerance} risk tolerance.
        """,
        agent=sentiment_agent,
        tools=[get_news_tool, analyze_sentiment_tool, scrape_tool],  # Use the new tool instances
        expected_output="A sentiment analysis summary with news highlights and a clear BUY/SELL recommendation."
    )

def create_fundamental_task(ticker, risk_tolerance="neutral"):
    risk_prompt = ""
    if risk_tolerance == "averse":
        risk_prompt = "Focus on financial stability, strong balance sheets, and consistent performance. "
    elif risk_tolerance == "seeking":
        risk_prompt = "Focus on growth potential, even if current financials are weaker. "
    else:
        risk_prompt = "Balance financial health with growth prospects. "

    return Task(
        description=f"""
        Conduct fundamental analysis of {ticker} based on available financial data using the FinancialDataTool.
        {risk_prompt}
        Analyze:
        - Revenue trends and growth
        - Profitability metrics
        - Cash flow stability
        - Balance sheet strength
        - Any areas of concern or competitive advantages.
        Use the FinancialDataTool's `get_financials` method to gather necessary data.

        Provide a BUY or SELL recommendation based on fundamental analysis and the {risk_tolerance} risk tolerance.
        """,
        agent=fundamental_agent,
        tools=[get_financials_tool, scrape_tool],  # Use the new tool instances
        expected_output="A comprehensive fundamental analysis with financial metrics and a clear BUY/SELL recommendation."
    )

def create_debate_task(ticker, risk_tolerance="neutral"):
    return Task(
        description=f"""
        Bought Price of the stock is 957.60
        Coordinate a debate among the valuation, sentiment, and fundamental analysts
        about {ticker} stock with {risk_tolerance} risk tolerance.

        Ensure each analyst presents their analysis and recommendation at least twice,
        using the information generated from their respective tasks.
        Facilitate discussion until consensus is reached.
        Consolidate all perspectives into a final comprehensive stock analysis report.

        The report should include:
        1. Executive summary with consensus recommendation
        2. Detailed analysis from each perspective
        3. Key positive indicators and concerns
        4. Final investment recommendation (BUY/SELL)
        5. Risk assessment aligned with the {risk_tolerance} profile

        Reply "TERMINATE" when the debate is complete and consensus is reached.
        """,
        agent=debate_manager,
        expected_output="A comprehensive stock analysis report with consensus recommendation and detailed rationale."
    )
# Create a function to run the multi-agent analysis for a given ticker
from tasks import create_valuation_task,create_sentiment_task,create_fundamental_task,create_debate_task
from crewai import Agent,Task,Crew,Process
from tools import get_stock_data_tool,get_financials_tool,calculate_metrics_tool,get_news_tool,analyze_sentiment_tool,scrape_tool
from agents import valuation_agent,sentiment_agent,fundamental_agent,debate_manager






def analyze_stock(ticker, risk_tolerance="neutral"):
    """
    Run multi-agent analysis for a given stock ticker
    """
    print(f"Starting analysis for {ticker} with {risk_tolerance} risk tolerance...")

    # Create tasks
    valuation_task = create_valuation_task(ticker, risk_tolerance)
    sentiment_task = create_sentiment_task(ticker, risk_tolerance)
    fundamental_task = create_fundamental_task(ticker, risk_tolerance)
    debate_task = create_debate_task(ticker, risk_tolerance)

    # Create crew
    crew = Crew(
        agents=[valuation_agent, sentiment_agent, fundamental_agent, debate_manager],
        tasks=[valuation_task, sentiment_task, fundamental_task, debate_task],
        verbose=True,
        process=Process.sequential  # Run tasks sequentially
    )

    # Execute the crew
    result = crew.kickoff()
    return result
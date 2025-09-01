# Define the agents with role prompting as described in the paper
from crewai import Agent
from tools import get_stock_data_tool,get_financials_tool,calculate_metrics_tool,get_news_tool,analyze_sentiment_tool,scrape_tool




# Valuation Agent
valuation_agent = Agent(
    role="Valuation Equity Analyst",
    goal="Analyze valuation trends of assets over extended time horizons, "
         "identify patterns in valuation metrics, and interpret implications for investors",
    backstory="Expert in technical analysis and quantitative finance with "
             "years of experience in identifying market trends and patterns",
    tools=[],  # Tools will be added through function calls
    verbose=True,
    allow_delegation=False,
    #llm=ChatOpenAI(model_name="gpt-4-turbo", temperature=0.1)
)

# Sentiment Agent
sentiment_agent = Agent(
    role="Sentiment Equity Analyst",
    goal="Analyze financial news, analyst ratings, and disclosures related to securities, "
         "and assess their implications and sentiment for investors",
    backstory="Seasoned analyst specializing in market sentiment and behavioral finance, "
             "with expertise in interpreting news impact on stock prices",
    tools=[scrape_tool],
    verbose=True,
    allow_delegation=False,
    #llm=ChatOpenAI(model_name="gpt-4-turbo", temperature=0.1)
)

# Fundamental Agent
fundamental_agent = Agent(
    role="Fundamental Financial Equity Analyst",
    goal="Analyze company fundamentals based on financial reports and disclosures, "
         "focusing on cash flow, income, operations, gross margin, and areas of concern",
    backstory="CFA with extensive experience in fundamental analysis and "
             "deep understanding of financial statements and business models",
    tools=[scrape_tool],
    verbose=True,
    allow_delegation=False,
    #llm=ChatOpenAI(model_name="gpt-4-turbo", temperature=0.1)
)

# Debate Manager Agent (for consensus building)
debate_manager = Agent(
    role="Debate Moderator",
    goal="Coordinate specialist agents to reach consensus on stock analysis, "
         "ensure all agents speak at least twice, and consolidate inputs into a final report",
    backstory="Experienced portfolio manager skilled at facilitating discussions "
             "among analysts with different perspectives and methodologies",
    verbose=True,
    allow_delegation=True,
    #llm=ChatOpenAI(model_name="gpt-4-turbo", temperature=0.1)
)
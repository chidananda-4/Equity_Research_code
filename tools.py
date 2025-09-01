# Define tools as classes inheriting from BaseTool
import yfinance as yf
import pandas as pd
import numpy as np
from crewai.tools import BaseTool
from langchain_community.tools.tavily_search import TavilySearchResults
from crewai_tools import ScrapeWebsiteTool, PDFSearchTool

class GetStockHistoricalDataTool(BaseTool):
    name: str = "Get Stock Historical Data"
    description: str = "Fetches historical stock data for a given ticker and period (e.g., '3mo'). Input: ticker, period (optional, default '3mo')."

    def _run(self, ticker: str, period: str = "3mo"):
        """Use the tool."""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            return hist.to_json() # Convert DataFrame to JSON string for easier handling by LLM
        except Exception as e:
            return f"Error fetching historical data for {ticker}: {e}"

class GetCompanyFinancialsTool(BaseTool):
    name: str = "Get Company Financials"
    description: str = "Fetches company financial statements (financials, balance sheet, cash flow) for a given ticker. Input: ticker."

    def _run(self, ticker: str):
        """Use the tool."""
        try:
            stock = yf.Ticker(ticker)
            financials = stock.financials.to_json()
            balance_sheet = stock.balance_sheet.to_json()
            cash_flow = stock.cashflow.to_json()
            return {
                'financials': financials,
                'balance_sheet': balance_sheet,
                'cash_flow': cash_flow
            }
        except Exception as e:
            return f"Error fetching financial data for {ticker}: {e}"

class CalculateFinancialMetricsTool(BaseTool):
    name: str = "Calculate Financial Metrics"
    description: str = "Calculates financial metrics like returns and volatility for a given ticker and period (e.g., '3mo'). Input: ticker, period (optional, default '3mo')."

    def _run(self, ticker: str, period: str = "3mo"):
        """Use the tool."""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)

            if len(hist) < 2:
                return {"error": "Insufficient data"}

            # Calculate returns and volatility
            daily_returns = hist['Close'].pct_change().dropna()
            cumulative_return = (hist['Close'].iloc[-1] / hist['Close'].iloc[0]) - 1
            n = len(daily_returns)

            # Annualized return (assuming 252 trading days)
            annualized_return = (1 + cumulative_return) ** (252/n) - 1 if n > 0 else 0

            # Annualized volatility
            daily_volatility = daily_returns.std()
            annualized_volatility = daily_volatility * np.sqrt(252)

            return {
                'cumulative_return': cumulative_return,
                'annualized_return': annualized_return,
                'daily_volatility': daily_volatility,
                'annualized_volatility': annualized_volatility,
                'price_data_sample': hist.head().to_json() # Return a sample as JSON
            }
        except Exception as e:
            return f"Error calculating metrics for {ticker}: {e}"

class NewsSearchTool(BaseTool):
    name: str = "News Search Tool"
    description: str = "Searches for recent news using Tavily Search API"

    

    def _run(self, ticker: str, max_results: int = 10) -> dict:
        """Search for recent news about a company using Tavily Search"""
        try:
            # Get company name first for better search results
            stock_info = yf.Ticker(ticker).info
            company_name = stock_info.get('longName', ticker)

            # Search for news about the company using Tavily
            search_query = f"{company_name} {ticker} stock news financial earnings"

            # Use Tavily's search with news focus
            tavily_tool = TavilySearchResults(max_results=5)
            results = tavily_tool.invoke(search_query)
            return results


            # Format results to match expected structure
            formatted_results = []
            for result in results.get('results', []):
                formatted_results.append({
                    'title': result.get('title', 'No title'),
                    'body': result.get('content', result.get('raw_content', 'No content')),
                    'date': self._extract_date(result),
                    'source': self._extract_source(result.get('url', '')),
                    'url': result.get('url', '')
                })

            return {"news": formatted_results}

        except Exception as e:
            print(f"Tavily search error: {e}")
            return {"error": f"Error searching news for {ticker}: {str(e)}", "news": []}

    def _extract_source(self, url: str) -> str:
        """Extract domain name from URL"""
        if not url:
            return "Unknown"
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except:
            return "Unknown"

    def _extract_date(self, result: dict) -> str:
        """Extract or infer date from result"""
        # Tavily doesn't always provide exact dates, so we can use current date as fallback
        return result.get('published_date', datetime.now().strftime('%Y-%m-%d'))

class SentimentAnalysisTool(BaseTool):
    name: str = "Sentiment Analysis Tool"
    description: str = "Analyzes sentiment from news articles"

    def _run(self, news_items: list) -> dict:
        """Enhanced sentiment analysis with Tavily results"""
        if not news_items:
            return {"sentiment_score": 0, "news_summaries": [], "detailed_news": []}

        positive_keywords = ['buy', 'strong', 'growth', 'positive', 'outperform',
                           'upgrade', 'bullish', 'profit', 'gain', 'beat', 'raise',
                           'strong buy', 'overweight', 'outperform', 'earnings beat',
                           'revenue growth', 'profitability', 'innovation']
        negative_keywords = ['sell', 'weak', 'decline', 'negative', 'underperform',
                           'downgrade', 'bearish', 'loss', 'drop', 'miss', 'cut',
                           'reduce', 'underweight', 'earnings miss', 'layoff',
                           'lawsuit', 'investigation', 'declining']

        sentiment_scores = []
        news_summaries = []
        detailed_news = []

        for item in news_items:
            title = item.get('title', '').lower()
            body = item.get('body', '').lower()
            date = item.get('date', '')
            source = item.get('source', '')
            url = item.get('url', '')

            text = title + " " + body

            positive_count = sum(1 for word in positive_keywords if word in text)
            negative_count = sum(1 for word in negative_keywords if word in text)

            score = positive_count - negative_count
            sentiment_scores.append(score)

            # Store detailed news info
            detailed_news.append({
                'title': item.get('title', 'No title'),
                'date': date,
                'source': source,
                'url': url,
                'sentiment_score': score,
                'positive_keywords': positive_count,
                'negative_keywords': negative_count
            })

            # Create summary of key news
            sentiment = "positive" if score > 0 else "negative" if score < 0 else "neutral"
            if abs(score) >= 1:  # Only include notable news
                news_summaries.append(f"{title[:100]}... ({sentiment}, score: {score}, {source})")

        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

        return {
            "sentiment_score": float(avg_sentiment),
            "news_summaries": news_summaries,
            "detailed_news": detailed_news,
            "total_articles": len(news_items),
            "positive_articles": sum(1 for score in sentiment_scores if score > 0),
            "negative_articles": sum(1 for score in sentiment_scores if score < 0),
            "neutral_articles": sum(1 for score in sentiment_scores if score == 0)
        }
# Initialize instances of the new BaseTool-derived classes
get_stock_data_tool = GetStockHistoricalDataTool()
get_financials_tool = GetCompanyFinancialsTool()
calculate_metrics_tool = CalculateFinancialMetricsTool()
get_news_tool = NewsSearchTool()
analyze_sentiment_tool = SentimentAnalysisTool()
scrape_tool = ScrapeWebsiteTool()

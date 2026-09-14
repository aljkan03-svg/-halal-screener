import yfinance as yf
import pandas as pd
from datetime import datetime

# ==========================================
# 1. Halal Assets List (Stocks & ETFs)
# ==========================================
HALAL_ASSETS = {
    "ETFs": ["HLAL", "SPUS", "UMMA", "SPSK"],
    "STOCKS": ["AAPL", "NVDA", "TSLA", "MSFT", "AMZN", "GOOGL", "AMD", "ADBE"]
}

# Keywords to track news regarding wars, geopolitical tensions, and market-moving events
WAR_AND_CRISIS_KEYWORDS = [
    "war", "conflict", "geopolitical", "tension", "military", 
    "sanctions", "strike", "defense", "crisis", "surge", "rally"
]

def check_halal_status(ticker_symbol):
    """Verify if the asset is in the approved halal list"""
    all_halal = HALAL_ASSETS["ETFs"] + HALAL_ASSETS["STOCKS"]
    if ticker_symbol.upper() in all_halal:
        return True
    return False

def analyze_stock_news(ticker_symbol):
    """Analyze news for war, crisis, or conflict triggers that might affect price momentum"""
    ticker = yf.Ticker(ticker_symbol)
    news_list = ticker.news
    
    alerts = []
    if news_list:
        for item in news_list:
            title = item.get('title', '')
            if not title and 'content' in item:
                title = item['content'].get('title', '')
                
            title_lower = title.lower()
            
            # Search for conflict or crisis keywords
            for keyword in WAR_AND_CRISIS_KEYWORDS:
                if keyword in title_lower:
                    alerts.append({
                        "keyword": keyword,
                        "title": title,
                        "link": item.get('link', item.get('url', 'N/A'))
                    })
                    break
    return alerts

def get_technical_signals(ticker_symbol):
    """Calculate basic technical indicators to assess price direction"""
    data = yf.download(ticker_symbol, period="6m", progress=False)
    if data.empty:
        return "No data available"
    
    # Calculate Moving Averages
    data['SMA50'] = data['Close'].rolling(window=50).mean()
    data['SMA200'] = data['Close'].rolling(window=200).mean()
    
    latest_close = data['Close'].iloc[-1]
    latest_sma50 = data['SMA50'].iloc[-1]
    
    if isinstance(latest_close, pd.Series):
        latest_close = latest_close.item()
    if isinstance(latest_sma50, pd.Series):
        latest_sma50 = latest_sma50.item()

    if latest_close > latest_sma50:
        return "Bullish Trend (Above 50 SMA)"
    else:
        return "Bearish / Consolidation (Below 50 SMA)"

def run_halal_market_tracker():
    """Execute comprehensive scan for all monitored halal assets"""
    print("=" * 60)
    print(f"Halal Market & Crisis Tracker - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    all_symbols = HALAL_ASSETS["ETFs"] + HALAL_ASSETS["STOCKS"]
    
    for symbol in all_symbols:
        print(f"\n[+] Scanning Asset: {symbol}")
        
        # 1. Shariah Compliance Check
        if check_halal_status(symbol):
            print("  |- Shariah Status: Halal (Verified List)")
        
        # 2. Technical Analysis
        signal = get_technical_signals(symbol)
        print(f"  |- Technical Signal: {signal}")
        
        # 3. News & Crisis Scan
        war_news = analyze_stock_news(symbol)
        if war_news:
            print("  |- ⚠️ Alert: Geopolitical/War-related triggers detected:")
            for news in war_news:
                print(f"     * [Keyword: {news['keyword']}] {news['title']}")
        else:
            print("  |- News Status: No active war or crisis news flags currently.")

if __name__ == "__main__":
    run_halal_market_tracker()

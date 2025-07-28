# pocket_option_scraper.py

import requests
import datetime

# Predefined list of OTC and major currency pairs
ASSETS = [
    # Major currency pairs
    "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "AUD/USD", "NZD/USD", "USD/CAD",
    
    # OTC assets (Pocket Option style)
    "EUR/JPY_otc", "GBP/JPY_otc", "AUD/JPY_otc", "USD/TRY_otc", "USD/ZAR_otc", 
    "EUR/USD_otc", "GBP/USD_otc", "AUD/USD_otc", "NZD/USD_otc", "USD/CAD_otc",
    "USD/CHF_otc", "USD/JPY_otc"
]

TIMEFRAME_MAP = {
    "1m": 60,
    "3m": 180,
    "5m": 300,
    "10m": 600
}

def fetch_candles(asset, timeframe="1m", limit=10):
    """
    Fetch real-time historical candle data from Pocket Option API endpoint.
    asset: e.g., 'EUR/USD', 'EUR/USD_otc'
    timeframe: '1m', '3m', '5m', '10m'
    """
    symbol = asset.replace("/", "").lower()
    if "otc" in asset.lower():
        symbol = symbol.replace("_otc", "") + "_otc"
    url = f"https://api.pocketoption.com/chart/history/{symbol}?period={TIMEFRAME_MAP[timeframe]}&limit={limit}"

    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        candles = []
        for i in range(len(data['t'])):
            candles.append({
                "time": datetime.datetime.utcfromtimestamp(data['t'][i]).strftime("%H:%M"),
                "open": data['o'][i],
                "close": data['c'][i],
                "high": data['h'][i],
                "low": data['l'][i],
                "volume": data['v'][i],
            })

        return candles
    except Exception as e:
        print(f"❌ Error fetching data for {asset}: {e}")
        return []

def get_all_assets():
    return ASSETS

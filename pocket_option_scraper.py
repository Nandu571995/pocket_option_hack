# pocket_option_scraper.py

import requests
import datetime

def fetch_candles(asset, timeframe="1m", limit=10):
    """
    Fetch real-time historical candle data from Pocket Option API endpoint.
    asset: e.g., 'EUR/USD', 'BTC/USD'
    timeframe: '1m', '3m', '5m', '10m'
    """
    symbol = asset.replace("/", "").lower()
    url = f"https://api.pocketoption.com/chart/history/{symbol}?period={timeframe}&limit={limit}"

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

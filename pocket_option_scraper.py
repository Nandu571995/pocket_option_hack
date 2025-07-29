import requests
import datetime
import pandas as pd

# ✅ Verified OTC, commodities, crypto assets from Pocket Option
ASSETS = [
    # Major OTC Forex Pairs
    "EUR/USD_otc", "GBP/USD_otc", "USD/JPY_otc", "AUD/USD_otc",
    "NZD/USD_otc", "USD/CHF_otc",

    # Popular Cross Pairs
    "GBP/JPY_otc", "CAD/JPY_otc", "AUD/NZD_otc", "EUR/GBP_otc",
    "NZD/JPY_otc", "EUR/JPY_otc",

    # Commodities (lowercase expected)
    "gold_otc", "silver_otc", "brent oil_otc", "natural gas_otc",

    # Crypto OTC (standard lowercase names)
    "bitcoin_otc", "ethereum_otc", "litecoin_otc"
]

# Map timeframes to Pocket Option API period values
TIMEFRAME_MAP = {
    "1m": 60,
    "3m": 180,
    "5m": 300,
    "10m": 600
}

def fetch_candles(asset, timeframe="1m", limit=100):
    """
    Fetch historical candle data from Pocket Option endpoint.
    """
    # Convert asset to Pocket Option symbol format
    symbol = asset.lower().replace("/", "").replace(" ", "").replace("_otc", "") + "_otc"

    url = f"https://api.pocketoption.com/chart/history/{symbol}?period={TIMEFRAME_MAP[timeframe]}&limit={limit}"

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()

        if "t" not in data:
            print(f"⚠️ No data for {asset}")
            return pd.DataFrame([])

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

        print(f"✅ {asset} — {len(candles)} candles fetched")
        return pd.DataFrame(candles)

    except Exception as e:
        print(f"❌ Error fetching data for {asset}: {e}")
        return pd.DataFrame([])

def get_candles(asset, timeframe="1m", limit=100):
    """
    External call used by strategy.py or pocket_bot.py
    """
    return fetch_candles(asset, timeframe, limit)

def get_all_assets():
    return ASSETS

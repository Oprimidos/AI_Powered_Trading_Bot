from binance.client import Client
import websockets
import json

import pandas as pd

# WebSocket URL for Binance Kline (Candle) data stream
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/{symbol}@kline_1s"

# Function to download crypto data via WebSocket
async def download_crypto_data(symbol):
    url = BINANCE_WS_URL.format(symbol=symbol.lower())  # Format symbol for WebSocket URL
    df = []
    
    try:
        # Connect to the WebSocket
        async with websockets.connect(url) as websocket:
            # Receive only one message and process it
            msg = await websocket.recv()
            data = json.loads(msg)  # Parse the JSON data

            # Extract kline (candlestick) data from the message
            kline = data['k']
            timestamp = pd.to_datetime(kline['t'], unit='ms')
            timestamp = timestamp.tz_localize("UTC").tz_convert("Europe/Istanbul")
            timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            open_price = float(kline['o'])
            close_price = float(kline['c'])
            high_price = float(kline['h'])
            low_price = float(kline['l'])
            volume = float(kline['v'])

            # Create a single row of data
            df.append({
            "Timestamp": timestamp,
            "Open": open_price,
            "High": close_price,
            "Low": high_price,
            "Close": low_price,
            "Volume": volume
            })

            df = pd.DataFrame(df)
                        
    except Exception as e:
        print(f"Error in WebSocket connection: {e}")

    # Return the DataFrame with the collected data
    return df

def download_crypto_data_interval(api_key, api_secret, symbol, interval="1m"):
    client = Client(api_key, api_secret)
    
    klines = client.get_historical_klines(symbol, interval, limit=1000)
    
    data = []
    for kline in klines:
        timestamp = pd.to_datetime(kline[0], unit='ms')
        timestamp = timestamp.tz_localize("UTC").tz_convert("Europe/Istanbul")
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        data.append({
            "Timestamp": timestamp,
            "Open": float(kline[1]),
            "High": float(kline[2]),
            "Low": float(kline[3]),
            "Close": float(kline[4]),
            "Volume": float(kline[5])
        })
    
    data = pd.DataFrame(data)
    
    return data


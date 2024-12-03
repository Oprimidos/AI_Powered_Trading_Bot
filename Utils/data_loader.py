from binance.client import Client
import websockets
import json
import pandas as pd

class DataLoader:
    
    # WebSocket URL for Binance Kline (Candle) data stream
    
    def __init__(self):
        self.BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/{symbol}@kline_1s"

    # Function to download crypto data via WebSocket
    # This function connects to the Binance WebSocket to fetch real-time kline data for the specified symbol.
    async def download_crypto_data(self,symbol):
        url = self.BINANCE_WS_URL.format(symbol=symbol.lower())  # Format symbol for WebSocket URL
        df = []  # Initialize an empty list to hold the data rows
        
        try:
            # Connect to the WebSocket
            async with websockets.connect(url) as websocket:
                # Receive only one message and process it
                msg = await websocket.recv()  # Receive data from the WebSocket
                data = json.loads(msg)  # Parse the JSON data

                # Extract kline (candlestick) data from the message
                kline = data['k']
                timestamp = pd.to_datetime(kline['t'], unit='ms')  # Convert the timestamp to a datetime object
                timestamp = timestamp.tz_localize("UTC").tz_convert("Europe/Istanbul")  # Convert timezone to Istanbul
                timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")  # Format timestamp as string
                open_price = float(kline['o'])  # Open price of the candle
                close_price = float(kline['c'])  # Close price of the candle
                high_price = float(kline['h'])  # High price of the candle
                low_price = float(kline['l'])  # Low price of the candle
                volume = float(kline['v'])  # Volume of trades during the candle

                # Create a single row of data and append it to the list
                df.append({
                    "Timestamp": timestamp,
                    "Open": open_price,
                    "High": close_price,
                    "Low": high_price,
                    "Close": low_price,
                    "Volume": volume
                })

                # Convert the list of rows to a DataFrame
                df = pd.DataFrame(df)
                            
        except Exception as e:
            # Handle any exceptions that occur during the WebSocket connection
            print(f"Error in WebSocket connection: {e}")

        # Return the DataFrame with the collected data
        return df

    # Function to download historical crypto data for a specific interval
    # This function uses the Binance REST API to fetch historical candlestick data.
    def download_crypto_data_interval(self,api_key, api_secret, symbol, interval="1m"):
        client = Client(api_key, api_secret)  # Initialize the Binance client with API credentials
        
        # Fetch historical kline data using the specified interval and symbol
        klines = client.get_historical_klines(symbol, interval, limit=100)
            
        data = []  # Initialize an empty list to hold the data rows
        for kline in klines:
            # Extract and process each kline entry
            timestamp = pd.to_datetime(kline[0], unit='ms')  # Convert the timestamp to a datetime object
            timestamp = timestamp.tz_localize("UTC").tz_convert("Europe/Istanbul")  # Convert timezone to Istanbul
            timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")  # Format timestamp as string
            data.append({
                "Timestamp": timestamp,
                "Open": float(kline[1]),  # Open price of the candle
                "High": float(kline[2]),  # High price of the candle
                "Low": float(kline[3]),  # Low price of the candle
                "Close": float(kline[4]),  # Close price of the candle
                "Volume": float(kline[5])  # Volume of trades during the candle
            })
            
        # Convert the list of rows to a DataFrame
        data = pd.DataFrame(data)
            
        # Return the DataFrame with the collected historical data
        return data
    
    def download_crypto_data_interval_backtest(self,api_key, api_secret, symbol, interval, check_date):
        client = Client(api_key, api_secret)  # Initialize the Binance client with API credentials
        
        # Fetch historical kline data using the specified interval and symbol
        klines = client.get_historical_klines(symbol, interval, check_date)
            
        data = []  # Initialize an empty list to hold the data rows
        for kline in klines:
            # Extract and process each kline entry
            timestamp = pd.to_datetime(kline[0], unit='ms')  # Convert the timestamp to a datetime object
            timestamp = timestamp.tz_localize("UTC").tz_convert("Europe/Istanbul")  # Convert timezone to Istanbul
            timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")  # Format timestamp as string
            data.append({
                "Timestamp": timestamp,
                "Open": float(kline[1]),  # Open price of the candle
                "High": float(kline[2]),  # High price of the candle
                "Low": float(kline[3]),  # Low price of the candle
                "Close": float(kline[4]),  # Close price of the candle
                "Volume": float(kline[5])  # Volume of trades during the candle
            })
            
        # Convert the list of rows to a DataFrame
        data = pd.DataFrame(data)
            
        # Return the DataFrame with the collected historical data
        return data
    
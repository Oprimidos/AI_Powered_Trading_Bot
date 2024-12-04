import pandas_ta as ta
import pandas as pd

class IndicatorCalculator:
    
    def __init__(self, rsi_length=14, macd_fast=12, macd_slow=26, macd_signal=9, adx_length=14):
        self.rsi_length = rsi_length
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal
        self.adx_length = adx_length

    def calculate_indicators(self, df):
        # Calculate RSI using the initialized rsi_length
        df['rsi'] = ta.rsi(df['Close'], length=self.rsi_length)
        
        # Calculate short and long term moving averages
        df['short_term_ma'] = df['Close'].rolling(window=self.rsi_length).mean()
        df['long_term_ma'] = df['Close'].rolling(window=2 * self.rsi_length).mean()

        # Calculate MACD Histogram using initialized macd_fast, macd_slow, and macd_signal
        macd = ta.macd(df['Close'], fast=self.macd_fast, slow=self.macd_slow, signal=self.macd_signal)
        df['macd'] = macd['MACDh_12_26_9']

        # Calculate ADX and its components using the initialized adx_length
        adx = ta.adx(df['High'], df['Low'], df['Close'], length=self.adx_length)
        df['adx'] = adx['ADX_14']  # Average Directional Index
        df['di_plus'] = adx['DMP_14']  # Positive Directional Indicator
        df['di_minus'] = adx['DMN_14']  # Negative Directional Indicator
        
        df.dropna(inplace=True)
        return df

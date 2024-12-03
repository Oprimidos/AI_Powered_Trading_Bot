import pandas_ta as ta
import pandas as pd

class IndicatorCalculator:
    
    def __init__(self):
        pass

    def calculate_indicators(self,df):
        # Calculate RSI
        df['rsi'] = ta.rsi(df['Close'], length=14)

        # Calculate MACD Histogram
        macd = ta.macd(df['Close'])
        df['macd'] = macd['MACDh_12_26_9']

        # Calculate ADX and its components
        adx = ta.adx(df['High'], df['Low'], df['Close'], length=14)
        df['adx'] = adx['ADX_14']  # Average Directional Index
        df['di_plus'] = adx['DMP_14']  # Positive Directional Indicator
        df['di_minus'] = adx['DMN_14']  # Negative Directional Indicator
        
        df.dropna(inplace=True)
        return df

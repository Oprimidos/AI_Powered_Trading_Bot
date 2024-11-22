import pandas_ta as ta
import pandas as pd

def calculate_indicators(df):
    # Calculate Bollinger Bands
    bb = ta.bbands(df['Close'], length=20)
    df = df.join(bb)
    

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

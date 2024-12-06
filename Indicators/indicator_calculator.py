import pandas as pd
import pandas_ta as ta

class IndicatorCalculator:
    def __init__(self, rsi_length=14, macd_fast=12, macd_slow=26, macd_signal=9, adx_length=14, stochastic_k=14, stochastic_d=3):
        self.rsi_length = rsi_length
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal
        self.adx_length = adx_length
        self.stochastic_k = stochastic_k
        self.stochastic_d = stochastic_d

    def verify_data(self, df):
        required_columns = ['Close', 'High', 'Low']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing columns in the DataFrame: {', '.join(missing_columns)}")

    def calculate_indicators(self, df):
        self.verify_data(df)

        # RSI
        df['rsi'] = ta.rsi(df['Close'], length=self.rsi_length)

        # Moving Averages
        df['short_term_ma'] = df['Close'].rolling(window=self.rsi_length).mean()
        df['long_term_ma'] = df['Close'].rolling(window=2 * self.rsi_length).mean()

        # MACD
        macd = ta.macd(df['Close'], fast=self.macd_fast, slow=self.macd_slow, signal=self.macd_signal)
        df['macd'] = macd['MACDh_12_26_9']

        # ADX
        adx = ta.adx(df['High'], df['Low'], df['Close'], length=self.adx_length)
        df['adx'] = adx['ADX_14']
        df['di_plus'] = adx['DMP_14']
        df['di_minus'] = adx['DMN_14']

        # Stochastic Oscillator
        stochastic = ta.stoch(df['High'], df['Low'], df['Close'], fast_k=self.stochastic_k, slow_d=self.stochastic_d)
        df['stoch_k'] = stochastic['STOCHk_14_3_3']
        df['stoch_d'] = stochastic['STOCHd_14_3_3']

        df.dropna(inplace=True)
        return df

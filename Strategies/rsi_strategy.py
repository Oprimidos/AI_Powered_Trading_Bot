from .strategy_interface import TradingStrategy
import pandas_ta as ta

class RSIStrategy(TradingStrategy):
    def __init__(self, stop_loss):
        super().__init__(stop_loss)
        self.rsi_lower = 30  # Default RSI lower bound
        self.rsi_upper = 70  # Default RSI upper bound

    def update_rsi_thresholds(self, market_volatility):
        """Dynamically adjust RSI thresholds based on market volatility."""
        if market_volatility > 0.05:  # Hypothetical high volatility threshold
            self.rsi_lower = 20
            self.rsi_upper = 80
        else:
            self.rsi_lower = 30
            self.rsi_upper = 70

    def label_logic(self, row):
        """Labeling logic for RSI strategy."""
        rsi = row['rsi']
        bollinger_low = row['bollinger_lband']
        bollinger_high = row['bollinger_hband']
        macd_line = row['macd']

        # Adjusted Buy Signal with Bollinger Bands and MACD
        if rsi < self.rsi_lower and row['Close'] < bollinger_low and macd_line > 0:
            return "Buy"

        # Adjusted Sell Signal with Bollinger Bands and MACD
        elif rsi > self.rsi_upper and row['Close'] > bollinger_high and macd_line < 0:
            return "Sell"

        return "Hold"

    def feature_columns(self):
        """Define the feature columns for the RSI strategy."""
        return ['rsi', 'bollinger_lband', 'bollinger_hband', 'macd', 'Close', 'Volume']

from .strategy_interface import TradingStrategy

class RSIStrategy(TradingStrategy):
    def __init__(self, stop_loss):
        super().__init__(stop_loss)

    def label_logic(self, row):
        """Labeling logic for RSI strategy."""
        rsi = row['rsi']
        adx = row['adx']
        volume = row['Volume']

        # Trending Market (ADX > 25)
        if adx > 25:
            if rsi < 30:  # Strongly oversold
                return "Buy"
            elif rsi > 70:  # Strongly overbought
                return "Sell"

        # Range-Bound Market (ADX < 20)
        elif adx < 20:
            if rsi < 35:  # Adjusted oversold threshold
                return "Buy"
            elif rsi > 65:  # Adjusted overbought threshold
                return "Sell"

        # Volume Confirmation (Optional: avoid low-liquidity signals)
        if volume < 10:  # Example threshold, adjust based on data
            return "Hold"

        # Default case
        return "Hold"

    def feature_columns(self):
        """Define the feature columns for the RSI strategy."""
        return ['rsi', 'adx', 'macd', 'Close', 'Volume']

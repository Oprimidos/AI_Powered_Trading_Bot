from .strategy_interface import TradingStrategy

class ADXStrategy(TradingStrategy):
    def __init__(self, stop_loss):
        super().__init__(stop_loss)

    def label_logic(self, row):
        """Labeling logic for ADX strategy."""
        adx = row['adx']
        rsi = row['rsi']
        di_plus = row['di_plus']
        di_minus = row['di_minus']

        # Buy Signal:
        if adx > 25 and di_plus > di_minus and rsi > 60:
            return "Buy"

        # Sell Signal:
        elif adx > 25 and di_minus > di_plus and rsi < 40:
            return "Sell"

        # Hold Signal:
        return "Hold"

    def feature_columns(self):
        """Define the feature columns for the ADX strategy."""
        return ['rsi', 'adx', 'di_plus', 'di_minus', 'macd', 'Close', 'Volume']

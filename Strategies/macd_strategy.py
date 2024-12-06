from .strategy_interface import TradingStrategy
import pandas_ta as ta

class MACDStrategy(TradingStrategy):
    def __init__(self, stop_loss):
        super().__init__(stop_loss)

    def label_logic(self, row):
        """Labeling logic for MACD strategy."""
        macd = row['macd']
        adx = row['adx']
        rsi = row['rsi']
        stochastic = row['stoch_k']  # Stochastic K line

        # Enhanced Buy Signal:
        if macd > 0 and rsi > 60 and adx > 25 and stochastic > 80:
            return "Buy"

        # Enhanced Sell Signal:
        elif macd < 0 and rsi < 40 and adx > 25 and stochastic < 20:
            return "Sell"

        # Hold Signal:
        return "Hold"

    def feature_columns(self):
        """Define the feature columns for the MACD strategy."""
        return ['macd', 'rsi', 'adx', 'stoch_k', 'Close', 'Volume']

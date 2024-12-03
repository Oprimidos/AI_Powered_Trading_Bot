from .strategy_interface import TradingStrategy
import pandas as pd

class MACDStrategy(TradingStrategy):
    def __init__(self, stop_loss, smoothing_period=14):
        super().__init__(stop_loss, smoothing_period)

    def label_logic(self, row):
        """Labeling logic for MACD strategy."""
        macd = row['macd']  # MACD Histogram value
        adx = row['adx']
        rsi = row['rsi']

        # Buy Signal:
        if macd > 0 and rsi > 60 and adx > 25:
            return "Buy"

        # Sell Signal:
        elif macd < 0 and rsi < 40 and adx > 25:
            return "Sell"

        # Hold Signal:
        return "Hold"

    def feature_columns(self):
        """Define the feature columns for the MACD strategy."""
        return ['macd', 'rsi', 'adx', 'Close', 'Volume']

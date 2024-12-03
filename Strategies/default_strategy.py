from .strategy_interface import TradingStrategy
import pandas as pd

class DefaultStrategy(TradingStrategy):
    def __init__(self, stop_loss):
        super().__init__(stop_loss)

    def label_logic(self, row):
        """Labeling logic for the Default strategy."""
        short_term_ma = row['short_term_ma']
        long_term_ma = row['long_term_ma']

        # Determine the trend
        if short_term_ma > long_term_ma:
            trend = 'uptrend'
        elif short_term_ma < long_term_ma:
            trend = 'downtrend'
        else:
            trend = 'sideways'

        rsi = row['rsi']

        # Decide the action based on trend and overbought/oversold conditions
        if trend == 'uptrend' and rsi < 70:
            return "Buy"
        elif trend == 'downtrend' and rsi > 30:
            return "Sell"
        return "Hold"

    def feature_columns(self):
        """Define the feature columns for the Default strategy."""
        return ['Close', 'rsi', 'Volume']

from .strategy_interface import TradingStrategy
import pandas_ta as ta

class ADXStrategy(TradingStrategy):
    def __init__(self, stop_loss, adx_threshold=25):
        super().__init__(stop_loss)
        self.adx_threshold = adx_threshold  # Dynamic ADX threshold

    def update_adx_threshold(self, market_volatility):
        """Dynamically adjust ADX threshold based on market volatility."""
        if market_volatility > 0.03:  # Hypothetical high volatility threshold
            self.adx_threshold = 30
        else:
            self.adx_threshold = 20

    def label_logic(self, row):
        """Labeling logic for ADX strategy."""
        adx = row['adx']
        di_plus = row['di_plus']
        di_minus = row['di_minus']
        rsi = row['rsi']

        # Buy Signal: Enhanced with dynamic ADX threshold
        if adx > self.adx_threshold and di_plus > di_minus and rsi > 60:
            return "Buy"

        # Sell Signal: Enhanced with dynamic ADX threshold
        elif adx > self.adx_threshold and di_minus > di_plus and rsi < 40:
            return "Sell"

        # Hold Signal: No strong directional movement
        return "Hold"

    def feature_columns(self):
        """Define the feature columns for the ADX strategy."""
        return ['adx', 'di_plus', 'di_minus', 'rsi', 'Close', 'Volume']

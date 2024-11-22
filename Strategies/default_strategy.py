from .strategy_interface import TradingStrategy

class DefaultStrategy(TradingStrategy):
    def __init__(self, stop_loss, smoothing_period=14):
        super().__init__(stop_loss, smoothing_period)

    def decide_action(self, row, df):
        # Calculate moving averages with smoothing
        short_term_ma = df['Close'].rolling(window=self.smoothing_period).mean().iloc[-1]
        long_term_ma = df['Close'].rolling(window=2 * self.smoothing_period).mean().iloc[-1]

        # Determine the trend
        if short_term_ma > long_term_ma:
            trend = 'uptrend'
        elif short_term_ma < long_term_ma:
            trend = 'downtrend'
        else:
            trend = 'sideways'

        # Use RSI to identify overbought/oversold conditions (with smoothing)
        smoothed_rsi = df['rsi'].rolling(window=self.smoothing_period).mean().iloc[-1]
        if smoothed_rsi > 70:
            overbought = True
            oversold = False
        elif smoothed_rsi < 30:
            overbought = False
            oversold = True
        else:
            overbought = False
            oversold = False

        print("Dataframe tail:", df.tail())

        # Decide the action based on trend and overbought/oversold conditions
        if trend == 'uptrend' and not overbought:
            print("Predicted action: Buy")
            return "Buy"
        elif trend == 'downtrend' and not oversold:
            print("Predicted action: Sell")
            return "Sell"
        else:
            print("Predicted action: Hold")
            return "Hold"

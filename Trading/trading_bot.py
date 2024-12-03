import asyncio
import time
import os
from Indicators import IndicatorCalculator
from Strategies import *
from Observer import Subject
from Utils import DataLoader
class TradingBot(Subject):
    """
    A trading bot implementation that uses strategies to make buy/sell/hold decisions.
    It also acts as a Subject in the Observer design pattern to notify observers about its state.
    """

    def __init__(self, coin_symbol):
        """
        Initialize the trading bot with the coin symbol and other necessary attributes.
        """
        self.strategy = None  # Strategy to be used for trading
        self.observers = []  # List of registered observers
        self.coin_symbol = coin_symbol  # The cryptocurrency symbol to trade
        self.df = None  # Dataframe to hold historical data
        self.api_key = os.getenv("BINANCE_API_KEY")  # Binance API Key from environment
        self.api_secret = os.getenv("BINANCE_API_SECRET")  # Binance API Secret from environment
        self.indicator_calculator = IndicatorCalculator()  # Indicator calculator object
        self.data_loader = DataLoader()  # Data loader objectt

    def get_latest_data(self):
        """
        Fetch the latest data for the selected cryptocurrency symbol using asyncio.
        """
        df = asyncio.run(self.data_loader.download_crypto_data(self.coin_symbol))
        self.df = df

    def get_interval_data(self):
        """
        Fetch the historical data for the selected cryptocurrency symbol using the REST
        API and return it as a DataFrame.
        """
        df = self.data_loader.download_crypto_data_interval(self.api_key, self.api_secret, self.coin_symbol)
        return df
    
    def set_coin_symbol(self, coin_symbol):
        """
        Update the cryptocurrency symbol to trade.
        """
        self.coin_symbol = coin_symbol

    def get_coin_symbol(self):
        """
        Get the current cryptocurrency symbol being traded.
        """
        return self.coin_symbol

    def register_observer(self, observer):
        """
        Add an observer to the list.
        """
        self.observers.append(observer)

    def remove_observer(self, observer):
        """
        Remove an observer from the list.
        """
        self.observers.remove(observer)

    def notify_observers(self, message):
        """
        Notify all registered observers with a message.
        """
        for observer in self.observers:
            observer.update(message)

    def set_strategy(self, strategy: TradingStrategy):
        """
        Set the trading strategy to be used.
        """
        self.strategy = strategy

    def trade(self, row, df):
        """
        Execute the trade action based on the current strategy.
        """
        if self.strategy:
            return self.strategy.execute_strategy(row,df)

    def evaluate_strategies(self, row, stop_loss, historical_data):
        """
        Dynamically evaluate and select the best strategy based on market conditions and historical data.
        """
        # Calculate market volatility
        volatility = historical_data['Close'].std()
        
        # Assign weights dynamically based on market conditions
        rsi_weight = 0.4 * (1 + volatility)
        macd_weight = 0.3 * (1 - volatility)
        adx_weight = 0.3 * volatility

        # Compute scores for each strategy
        rsi_score = row['rsi'] - historical_data['rsi'].mean()
        macd_score = row['macd'] - historical_data['macd'].mean()
        adx_score = row['adx'] - historical_data['adx'].mean()

        # Calculate weighted scores
        weighted_scores = [rsi_score * rsi_weight, macd_score * macd_weight, adx_score * adx_weight]

        # Choose the strategy with the highest score
        if max(weighted_scores) > 0:
            if weighted_scores.index(max(weighted_scores)) == 0:
                return RSIStrategy(stop_loss)
            elif weighted_scores.index(max(weighted_scores)) == 1:
                return MACDStrategy(stop_loss)
            else:
                return ADXStrategy(stop_loss)
        else:
            return DefaultStrategy(stop_loss)

    def change_strategy(self, row, stop_loss, df):
        """
        Evaluate and change the trading strategy dynamically.
        """
        best_strategy = self.evaluate_strategies(row, stop_loss, df)
        self.set_strategy(best_strategy)

    def simulate_trading(self, initial_balance, stop_loss, interval):
        """
        Simulate trading based on the selected strategy and notify observers about the process.
        """
        balance = initial_balance  # Initialize the starting balance
        position = 0  # Current trading position (amount of cryptocurrency held)
        entry_price = 0  # Entry price for the trade
        trades = []  # Record of trades performed during the simulation
        first_trade = True  # Flag to ensure the first action is a "Buy"

        start_time = time.time()  # Record the start time of the simulation

        while True:
            # Calculate the elapsed time
            elapsed_time = time.time() - start_time

            # Step 1: Fetch the latest market data
            self.get_latest_data()
            print("Acquired Data")

            # Step 2: Get the latest row and calculate indicators
            row = self.df.iloc[-1]
            df = self.get_interval_data()
            df.loc[len(df)] = row
            df = self.indicator_calculator.calculate_indicators(df)
            print("Calculated Indicators")

            # Step 3: Evaluate and change strategy dynamically
            row = df.iloc[-1]
            self.change_strategy(row, stop_loss, df)

            # Step 4: Take action based on the strategy
            if first_trade:
                # Ensure the first trade is a "Buy"
                action = "Buy"
                print("First trade, Buying...")
                first_trade = False
            else:
                # Follow the strategy after the first trade
                action = self.trade(row, df)

            if action == "Buy":
                if position == 0:
                    # Open a new position
                    entry_price = row['Close']
                    position = balance / entry_price
                    trades.append(("BUY", entry_price, balance))
                    print(f"Bought {self.coin_symbol}, Current balance is: {balance}, Current Strategy: {self.strategy.__class__.__name__}")
                    self.notify_observers(f"Bought {self.coin_symbol}, Current balance is: {balance}")
                else:
                    print("Could't buy, Current Strategy: ", self.strategy.__class__.__name__)
            elif action == "Sell":
                if position > 0:
                    # Close the existing position
                    sell_price = row['Close']
                    balance = position * sell_price
                    trades.append(("SELL", sell_price, balance))
                    print(f"Sold {self.coin_symbol}, Current balance is: {balance}, Current Strategy: {self.strategy.__class__.__name__}")
                    position = 0
                    self.notify_observers(f"Sold {self.coin_symbol}, Current balance is: {balance}")
                else:
                    print("Could't sell, Current Strategy: ", self.strategy.__class__.__name__)
            elif action == "Hold":
                print("Holding, Current Strategy: ", self.strategy.__class__.__name__)

            # Step 5: Stop the simulation after the specified interval
            if elapsed_time > interval:
                break

        # Notify observers of the simulation's completion
        elapsed_time = time.time() - start_time
        self.notify_observers("Simulation complete")
        return f"Remaining balance: {balance}$, Trading count: {len(trades)}, Profit/Loss: {balance - initial_balance}$"

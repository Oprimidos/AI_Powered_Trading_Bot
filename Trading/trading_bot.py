import asyncio
import time
import os
from Indicators.indicator_calculator import calculate_indicators
from Strategies import *
from Observer import Subject
from Utils.data_loader import download_crypto_data
from Utils.data_loader import download_crypto_data_interval

class TradingBot(Subject):
    def __init__(self, coin_symbol):
        self.strategy = None
        self.observers = []
        self.coin_symbol = coin_symbol
        self.df = None
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")

    def get_latest_data(self):
        df = asyncio.run(download_crypto_data(self.coin_symbol))
        self.df = df

    def get_interval_data(self):
        df = download_crypto_data_interval(self.api_key, self.api_secret, self.coin_symbol)
        return df

    def set_coin_symbol(self, coin_symbol):
        self.coin_symbol = coin_symbol

    def get_coin_symbol(self):
        return self.coin_symbol

    def register_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

    def set_strategy(self, strategy: TradingStrategy):
        self.strategy = strategy

    def trade(self, row, df):
        if self.strategy:
            return self.strategy.decide_action(row,df)

    def evaluate_strategies(self, row, stop_loss, historical_data):
        # Calculate dynamic weights based on market conditions
        volatility = historical_data['Close'].std()
        rsi_weight = 0.4 * (1 + volatility)
        macd_weight = 0.3 * (1 - volatility)
        adx_weight = 0.3 * volatility

        # Calculate weighted scores for each strategy
        rsi_score = row['rsi'] - historical_data['rsi'].mean()
        macd_score = row['macd'] - historical_data['macd'].mean()
        adx_score = row['adx'] - historical_data['adx'].mean()

        weighted_scores = [rsi_score * rsi_weight, macd_score * macd_weight, adx_score * adx_weight]

        # Select the strategy with the highest weighted score
        if max(weighted_scores) > 0:
            if weighted_scores.index(max(weighted_scores)) == 0:
                return RSIStrategy(stop_loss)
            elif weighted_scores.index(max(weighted_scores)) == 1:
                return MACDStrategy(stop_loss)
            else:
                return ADXStrategy(stop_loss)
        else:
            return DefaultStrategy(stop_loss)


    
    def change_strategy(self, row, stop_loss,df):
        best_strategy = self.evaluate_strategies(row, stop_loss,df)
        self.set_strategy(best_strategy)

    def simulate_trading(self, initial_balance, stop_loss, interval):
        
        balance = initial_balance
        position = 0
        entry_price = 0
        trades = []

        start_time = time.time()


        while True:
            
            elapsed_time = time.time() - start_time
            self.get_latest_data()
            print("Acquired Data")
            row = self.df.iloc[-1]
            df = self.get_interval_data()
            df.loc[len(df)] = row
            df = calculate_indicators(df)
            print("Calculated Indicators")
            row = df.iloc[-1]
            self.change_strategy(row, stop_loss,df)
            action = self.trade(row,df)
            if action == "Buy":
                if position == 0:
                    entry_price = row['Close']
                    position = balance / entry_price
                    trades.append(("BUY", entry_price, balance))
                    print(f"Bought {self.coin_symbol}, Current balance is: {balance}, Current Strategy: {self.strategy.__class__.__name__}")
                    self.notify_observers(f"Bought {self.coin_symbol}, Current balance is: {balance}")
                else:
                    print("Could't buy, Current Strategy: ", self.strategy.__class__.__name__)
            elif action == "Sell":
                if position > 0:
                    sell_price = row['Close']
                    balance = position * sell_price
                    trades.append(("SELL", sell_price, balance))
                    print(f"Sold {self.coin_symbol}, Current balance is: {balance}, Current Strategy: {self.strategy.__class__.__name__}")
                    position = 0
                    self.notify_observers(f"Sold {self.coin_symbol}, Current balance is: {balance}")
                else:  
                    print("Could't sell, Current Strategy: ", self.strategy.__class__.__name__)
            elif action == "Hold":
                if position == 0:
                    entry_price = row['Close']
                    position = balance / entry_price
                    trades.append(("BUY", entry_price, balance))
                    print(f"Bought {self.coin_symbol} (Hold triggered buy), Current balance is: {balance}, Current Strategy: {self.strategy.__class__.__name__}")
                    self.notify_observers(f"Bought {self.coin_symbol}, Current balance is: {balance}")
                else:
                    print("Holding, Current Strategy: ", self.strategy.__class__.__name__)

            if elapsed_time > interval:
                break

        elapsed_time = time.time() - start_time
        self.notify_observers("Simulation complete")
        return f"Kalan bakiye: {balance}$, İşlem sayısı: {len(trades)}, Kar/Zarar: {balance - initial_balance}$"

    

import matplotlib.pyplot as plt
from .observer import Observer

class VisualizationObserver(Observer):
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        # Ensure only one instance of the class is created
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Check if instance is already initialized
        if not hasattr(self, "initialized"):
            self.trade_counter = 0  # Initialize the trade counter
            self.balances = []  # Track balance cumulatively
            self.actions = []  # Stores actions like "Buy", "Sell", "Hold"
            self.initialized = True

    def update(self, message):
        if "Bought" in message or "Sold" in message:
            # During each trade, we only store the trade count and balance
            parts = message.split(", ")
            balance_part = parts[1].split(": ")[1]  # Extract the balance part "Current balance is: {balance}"
            
            # Extract the balance as float
            balance = float(balance_part)
            
            # Increment the trade counter
            self.trade_counter += 1

            # Append the balance to the balances list
            self.balances.append(balance)

        elif "Simulation complete" in message:
            # Plot data when simulation ends
            self._plot_balances()

    def _plot_balances(self):
        """Plot the balance changes over trades at the end of the simulation."""
        # Create a plot showing the balance change over time (across trades)
        plt.plot(range(1, self.trade_counter + 1), self.balances, label="Balance Over Time")
        
        # Set axis labels and title
        plt.title("Trading Simulation Visualization")
        plt.xlabel("Trade Number")
        plt.ylabel("Balance")
        plt.legend()
        
        # Display the plot
        plt.show()

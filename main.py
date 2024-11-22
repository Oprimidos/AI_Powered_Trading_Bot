import tkinter as tk
from tkinter import ttk, messagebox
from Utils.data_loader import download_crypto_data
from Indicators.indicator_calculator import calculate_indicators
from Trading.trading_bot import TradingBot
from Observer import VisualizationObserver
from Observer import LoggingObserver
import pandas as pd

class TradingBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Trading Bot")
        
        # Styling
        self.root.config(bg="#2c3e50")  # Dark background for that techy look
        self.font_style = ("Arial", 12)
        self.header_font = ("Arial", 14, "bold")
        self.button_style = {"width": 20, "relief": "raised", "bd": 2}
        
        # Apply styles for ttk widgets
        style = ttk.Style()
        style.configure("TFrame", background="#2c3e50")  # Dark background for frames
        style.configure("TButton", background="#f39c12", foreground="black", font=("Arial", 12))
        style.configure("TLabel", background="#2c3e50", foreground="white", font=("Arial", 12))
        style.configure("TEntry", background="#34495e", foreground="black", font=("Arial", 12), padding=5)

        # Initial balance state
        self.current_balance = 10000  # Default initial balance
        
        # Main Frame
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Frame for Symbol selection
        symbol_frame = ttk.Frame(main_frame, style="TFrame")
        symbol_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
        
        ttk.Label(symbol_frame, text="Select Cryptocurrency Symbol:", style="TLabel").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.symbol_var = tk.StringVar()
        self.symbol_dropdown = ttk.Combobox(symbol_frame, textvariable=self.symbol_var, values=["BTCUSDT", "ETHUSDT", "BNBUSDT"], state="readonly", font=self.font_style)
        self.symbol_dropdown.grid(row=0, column=1, padx=10, pady=5)
        
        # Frame for Balance and Stop Loss
        balance_stoploss_frame = ttk.Frame(main_frame, style="TFrame")
        balance_stoploss_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        
        ttk.Label(balance_stoploss_frame, text="Current Balance:", style="TLabel").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.balance_label = ttk.Label(balance_stoploss_frame, text=f"${self.current_balance}", style="TLabel", foreground="#27ae60")
        self.balance_label.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(balance_stoploss_frame, text="Stop Loss (in percentage):", style="TLabel").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.stop_loss_var = tk.StringVar(value="2")  # Default to 2% stop loss
        self.stop_loss_entry = ttk.Entry(balance_stoploss_frame, textvariable=self.stop_loss_var, font=self.font_style, width=10)
        self.stop_loss_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(balance_stoploss_frame, text="Interval (in minutes):", style="TLabel").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.interval_var = tk.StringVar(value="5")  # Default to 5 minutes interval
        self.interval_entry = ttk.Entry(balance_stoploss_frame, textvariable=self.interval_var, font=self.font_style, width=10)
        self.interval_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Run Trading Bot Button
        self.fetch_data_button = ttk.Button(main_frame, text="Run Trading Bot", command=self.fetch_data, style="TButton")
        self.fetch_data_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Output label
        self.output_label = ttk.Label(main_frame, text="", style="TLabel", wraplength=400)
        self.output_label.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
    
    def fetch_data(self):
        symbol = self.symbol_var.get()
        try:
            stop_loss_percentage = int(self.stop_loss_var.get())  # Convert to integer
            if stop_loss_percentage <= 0:
                raise ValueError("Stop loss must be a positive integer.")
            stop_loss = stop_loss_percentage / 100  # Convert to decimal
        except ValueError as ve:
            messagebox.showerror("Input Error", f"Please enter a valid positive integer for stop loss. {ve}")
            return
        
        try:
            interval_minutes = int(self.interval_var.get())  # Get interval from the user
            if interval_minutes <= 0:
                raise ValueError("Interval must be a positive integer.")
            interval = interval_minutes * 60  # Convert minutes to seconds
        except ValueError as ve:
            messagebox.showerror("Input Error", f"Please enter a valid positive integer for interval. {ve}")
            return
        
        if not symbol:
            messagebox.showerror("Input Error", "Please select a symbol.")
            return
        
        try:
            # Step 3: Initialize trading bot and observers
            trading_bot = TradingBot(symbol)
            visualizer = VisualizationObserver()
            logging_observer = LoggingObserver()
            
            trading_bot.register_observer(visualizer)
            trading_bot.register_observer(logging_observer)
            
            # Step 4: Simulate trading
            self.output_label.config(text="Trading...")
            self.root.update()
            final_report = trading_bot.simulate_trading(self.current_balance, stop_loss,interval)
            
            # Update the current balance
            self.current_balance = float(final_report.split(",")[0].split(":")[1].strip("$"))
            self.balance_label.config(text=f"${self.current_balance}")
            
            # Step 5: Display the final report
            self.output_label.config(text=f"Trading Complete!\n{final_report}")
            messagebox.showinfo("Trading Complete", final_report)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotApp(root)
    root.mainloop()

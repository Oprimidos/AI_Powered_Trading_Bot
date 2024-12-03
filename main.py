import tkinter as tk
from tkinter import ttk, messagebox
from Trading.trading_bot import TradingBot
from Observer import VisualizationObserver, LoggingObserver

class TradingBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Trading Bot")
        self.root.geometry("500x450")
        
        # Styling
        self.root.config(bg="#1c1e26")
        self.font_style = ("Arial", 12)
        self.header_font = ("Arial", 14, "bold")
        
        # Apply modern styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#1c1e26")
        self.style.configure("TButton", background="#00bcd4", foreground="white", font=("Arial", 12), padding=6)
        self.style.map("TButton", background=[("active", "#0097a7")])
        self.style.configure("TLabel", background="#1c1e26", foreground="white", font=("Arial", 12))
        self.style.configure("TEntry", padding=6, relief="flat", font=("Arial", 12))
        self.style.configure("TCombobox", font=("Arial", 12), padding=6)
        
        # Initial screen for mode selection
        self.mode_selection_frame = ttk.Frame(self.root, style="TFrame", padding=15)
        self.mode_selection_frame.pack(fill="both", expand=True)
        
        ttk.Label(self.mode_selection_frame, text="Select Mode", style="TLabel").pack(pady=10)
        
        self.trade_mode_var = tk.StringVar(value="backtest")
        
        # Modern Toggle Buttons for mode selection
        self.mode_buttons_frame = ttk.Frame(self.mode_selection_frame, style="TFrame")
        self.mode_buttons_frame.pack(pady=20)

        self.live_trade_button = ttk.Button(self.mode_buttons_frame, text="Live Trade", 
                                            style="TButton", command=lambda: self.toggle_mode("live"))
        self.live_trade_button.grid(row=0, column=0, padx=20, pady=10)

        self.backtest_button = ttk.Button(self.mode_buttons_frame, text="Backtest", 
                                          style="TButton", command=lambda: self.toggle_mode("backtest"))
        self.backtest_button.grid(row=0, column=1, padx=20, pady=10)

        select_button = ttk.Button(self.mode_selection_frame, text="Select", command=self.open_trading_gui)
        select_button.pack(pady=20)

    def toggle_mode(self, mode):
        """Function to toggle between 'Live Trade' and 'Backtest'."""
        self.trade_mode_var.set(mode)
        
        # Reset styles for both buttons
        self.live_trade_button.config(style="TButton")
        self.backtest_button.config(style="TButton")
        
        # Highlight the selected mode button
        if mode == "live":
            self.style.configure("Backtest.TButton", background="#00bcd4", foreground="white")
            self.style.configure("Live.TButton", background="gray", foreground="white")  # Active button color
            self.live_trade_button.config(style="Live.TButton")
            self.backtest_button.config(style="Backtest.TButton")
        else:
            self.style.configure("Live.TButton", background="#00bcd4", foreground="white")  
            self.style.configure("Backtest.TButton", background="gray", foreground="white")  # Active button color
            self.backtest_button.config(style="Backtest.TButton")
            self.live_trade_button.config(style="Live.TButton")


    def open_trading_gui(self):
        # Hide the initial mode selection screen
        self.mode_selection_frame.pack_forget()

        # Now, show the trading bot GUI based on the selected mode
        self.main_frame = ttk.Frame(self.root, style="TFrame", padding=15)
        self.main_frame.pack(fill="both", expand=True)
        
        # Symbol selection
        symbol_frame = ttk.Frame(self.main_frame, style="TFrame", padding=10)
        symbol_frame.pack(fill="x", pady=10)
        ttk.Label(symbol_frame, text="Cryptocurrency Symbol:", style="TLabel").pack(anchor="w")
        self.symbol_var = tk.StringVar()
        self.symbol_dropdown = ttk.Combobox(symbol_frame, textvariable=self.symbol_var, 
                                            values=["BTCUSDT", "ETHUSDT", "BNBUSDT"], 
                                            state="readonly")
        self.symbol_dropdown.pack(fill="x", pady=5)

        self.current_balance = 10000  # Initial balance

        # Balance and Stop Loss
        balance_frame = ttk.Frame(self.main_frame, style="TFrame", padding=10)
        balance_frame.pack(fill="x", pady=10)
        ttk.Label(balance_frame, text="Current Balance:", style="TLabel").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.balance_label = ttk.Label(balance_frame, text=f"${self.current_balance}", style="TLabel", foreground="#4caf50")
        self.balance_label.grid(row=0, column=1, sticky="e", padx=5, pady=5)
        
        ttk.Label(balance_frame, text="Stop Loss (%):", style="TLabel").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.stop_loss_var = tk.StringVar(value="2")
        self.stop_loss_entry = ttk.Entry(balance_frame, textvariable=self.stop_loss_var)
        self.stop_loss_entry.grid(row=1, column=1, sticky="e", padx=5, pady=5)
        
        # Show/Hide Interval and Lookback Days frame depending on the selected mode
        self.mode_specific_frame = ttk.Frame(self.main_frame, style="TFrame", padding=10)
        
        if self.trade_mode_var.get() == "live":
        
            ttk.Label(self.mode_specific_frame, text="Interval (mins):", style="TLabel").grid(row=0, column=0, sticky="w", padx=5, pady=5)
            self.interval_var = tk.StringVar(value="5")
            self.interval_dropdown = ttk.Combobox(self.mode_specific_frame, textvariable=self.interval_var, 
                                                values=["1", "3", "5", "15", "30"], 
                                                state="readonly")
            self.interval_dropdown.grid(row=0, column=1, sticky="e", padx=5, pady=5)
            self.mode_specific_frame.pack(fill="x", pady=10)
        
        else:
            
            ttk.Label(self.mode_specific_frame, text="Kindle Intervals:", style="TLabel").grid(row=0, column=0, sticky="w", padx=5, pady=5)
            self.interval_var = tk.StringVar(value="1m")
            self.interval_dropdown = ttk.Combobox(self.mode_specific_frame, textvariable=self.interval_var, 
                                                values=["1m", "5m", "30m", "1h", "1d","1w","1M"], 
                                                state="readonly")
            self.interval_dropdown.grid(row=0, column=1, sticky="e", padx=5, pady=5)
            self.mode_specific_frame.pack(fill="x", pady=10)

            ttk.Label(self.mode_specific_frame, text="Trade Interval:", style="TLabel").grid(row=1, column=0, sticky="w", padx=5, pady=5)
            self.lookback_days_var = tk.StringVar(value="1 hour ago UTC")
            self.lookback_days_dropdown = ttk.Combobox(self.mode_specific_frame, textvariable=self.lookback_days_var, 
                                                    values=["1 hour ago UTC", "1 day ago UTC", "1 month ago UTC", "1 year ago UTC"], 
                                                    state="readonly")
            self.lookback_days_dropdown.grid(row=1, column=1, sticky="e", padx=5, pady=5)
                
        # Run Trading Bot Button
        self.fetch_data_button = ttk.Button(self.main_frame, text="Run Trading Bot", command=self.fetch_data)
        self.fetch_data_button.pack(pady=20)

        # Output label
        self.output_label = ttk.Label(self.main_frame, text="", style="TLabel", wraplength=400)
        self.output_label.pack(fill="x", pady=10)

    def fetch_data(self):
        symbol = self.symbol_var.get()
        trade_mode = self.trade_mode_var.get()  # Live or Backtest
        try:
            stop_loss_percentage = int(self.stop_loss_var.get())  # Convert to integer
            if stop_loss_percentage <= 0:
                raise ValueError("Stop loss must be a positive integer.")
            stop_loss = stop_loss_percentage / 100  # Convert to decimal
        except ValueError as ve:
            messagebox.showerror("Input Error", f"Please enter a valid positive integer for stop loss. {ve}")
            return

        try:
            if trade_mode == "live":
                interval_minutes = int(self.interval_var.get())  # Get interval from the user
                if interval_minutes <= 0:
                    raise ValueError("Interval must be a positive integer.")
                interval = interval_minutes * 60  # Convert minutes to seconds
                lookback_days = None  # Not needed for live mode
            else:
                interval = str(self.interval_var.get())
                lookback_days = str(self.lookback_days_var.get()) 

        except ValueError as ve:
            messagebox.showerror("Input Error", f"Please enter a valid value. {ve}")
            return

        if not symbol:
            messagebox.showerror("Input Error", "Please select a cryptocurrency symbol.")
            return
        
        try:
            trading_bot = TradingBot(coin_symbol=symbol)
            
            visualizer = VisualizationObserver()
            logger = LoggingObserver()

            trading_bot.register_observer(visualizer)
            trading_bot.register_observer(logger)

            if trade_mode == "live":
                result = trading_bot.simulate_trading(interval=interval, stop_loss=stop_loss, initial_balance=self.current_balance)
            else:
                result = trading_bot.backtest_trading(interval=interval, check_date=lookback_days, stop_loss=stop_loss, initial_balance=self.current_balance)
            print(result)
            self.current_balance = result
            self.balance_label.config(text=f"${self.current_balance}")
            messagebox.showinfo("Trading Bot", "Trading Bot has finished running.")

        except Exception as e:
            messagebox.showerror("Input Error", f"Invalid input for mode-specific settings.\n{e}")



root = tk.Tk()
icon = tk.PhotoImage(file="icon.png")
root.iconphoto(False, icon)
app = TradingBotApp(root)
root.mainloop()

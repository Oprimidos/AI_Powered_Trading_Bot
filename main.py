import tkinter as tk
from tkinter import ttk, messagebox
from Trading.trading_bot import TradingBot
from Observer import VisualizationObserver
from Observer import LoggingObserver

class TradingBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Trading Bot")
        self.root.geometry("500x400")
        
        # Styling
        self.root.config(bg="#1c1e26")
        self.font_style = ("Arial", 12)
        self.header_font = ("Arial", 14, "bold")
        
        # Apply modern styles
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#1c1e26")
        style.configure("TButton", background="#00bcd4", foreground="white", font=("Arial", 12), padding=6)
        style.map("TButton", background=[("active", "#0097a7")])
        style.configure("TLabel", background="#1c1e26", foreground="white", font=("Arial", 12))
        style.configure("TEntry", padding=6, relief="flat", font=("Arial", 12))
        style.configure("TCombobox", font=("Arial", 12), padding=6)
        
        # Frame
        main_frame = ttk.Frame(self.root, style="TFrame", padding=15)
        main_frame.pack(fill="both", expand=True)

        # Symbol selection
        symbol_frame = ttk.Frame(main_frame, style="TFrame", padding=10)
        symbol_frame.pack(fill="x", pady=10)
        ttk.Label(symbol_frame, text="Cryptocurrency Symbol:", style="TLabel").pack(anchor="w")
        self.symbol_var = tk.StringVar()
        self.symbol_dropdown = ttk.Combobox(symbol_frame, textvariable=self.symbol_var, 
                                            values=["BTCUSDT", "ETHUSDT", "BNBUSDT"], 
                                            state="readonly")
        self.symbol_dropdown.pack(fill="x", pady=5)

        self.current_balance = 10000  # Initial balance

        # Balance and Stop Loss
        balance_frame = ttk.Frame(main_frame, style="TFrame", padding=10)
        balance_frame.pack(fill="x", pady=10)
        ttk.Label(balance_frame, text="Current Balance:", style="TLabel").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.balance_label = ttk.Label(balance_frame, text=f"${self.current_balance}", style="TLabel", foreground="#4caf50")
        self.balance_label.grid(row=0, column=1, sticky="e", padx=5, pady=5)
        
        ttk.Label(balance_frame, text="Stop Loss (%):", style="TLabel").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.stop_loss_var = tk.StringVar(value="2")
        self.stop_loss_entry = ttk.Entry(balance_frame, textvariable=self.stop_loss_var)
        self.stop_loss_entry.grid(row=1, column=1, sticky="e", padx=5, pady=5)
        
        ttk.Label(balance_frame, text="Interval (mins):", style="TLabel").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.interval_var = tk.StringVar(value="5")
        self.interval_entry = ttk.Entry(balance_frame, textvariable=self.interval_var)
        self.interval_entry.grid(row=2, column=1, sticky="e", padx=5, pady=5)
        
        # Run Trading Bot Button
        self.fetch_data_button = ttk.Button(main_frame, text="Run Trading Bot", command=self.fetch_data)
        self.fetch_data_button.pack(pady=20)

        # Output label
        self.output_label = ttk.Label(main_frame, text="", style="TLabel", wraplength=400)
        self.output_label.pack(fill="x", pady=10)

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
            # Step 1: Initialize trading bot and observers
            trading_bot = TradingBot(symbol)
            visualizer = VisualizationObserver()
            logging_observer = LoggingObserver()

            trading_bot.register_observer(visualizer)
            trading_bot.register_observer(logging_observer)

            # Step 2: Simulate trading
            self.output_label.config(text="Trading...")
            self.root.update()
            final_report = trading_bot.simulate_trading(self.current_balance, stop_loss, interval)

            # Update the current balance
            self.current_balance = float(final_report.split(",")[0].split(":")[1].strip("$"))
            self.balance_label.config(text=f"${self.current_balance}")

            # Step 3: Display the final report
            self.output_label.config(text=f"Trading Complete!")
            messagebox.showinfo("Trading Complete", final_report)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotApp(root)
    root.mainloop()

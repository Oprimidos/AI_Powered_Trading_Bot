# Trading Bot Project

This project is a trading bot that uses various trading strategies to make buy and sell decisions based on cryptocurrency data.

## Table of Contents

-  [Installation](#installation)
-  [Usage](#usage)
-  [Configuration](#configuration)
-  [Strategies](#strategies)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/trading-bot-project.git
   cd trading-bot-project
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:

   On Windows:

   ```bash
   .venv\Scripts\activate
   ```

   On macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Set your Binance API key and secret as environment variables:

   On Windows:

   ```bash
   setx BINANCE_API_KEY "your_api_key_here"
   setx BINANCE_API_SECRET "your_api_secret_here"
   ```

   On macOS/Linux:

   ```bash
   export BINANCE_API_KEY="your_api_key_here"
   export BINANCE_API_SECRET="your_api_secret_here"
   ```

2. Run the trading bot:
   ```bash
   python main.py
   ```

## Configuration

1. Add your cryptocurrency symbols in the [main.py](http://_vscodecontentref_/1) file:

   ```python
   symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']  # Add your cryptocurrency symbols here
   ```

## Strategies

The bot currently supports the following strategies:

-  **MACD Strategy**: Moving Average Convergence Divergence
-  **RSI Strategy**: Relative Strength Index
-  **ADX Strategy**: Average Directional Index
-  **Default Strategy**: Default Strategy For Holding If No Strategies Above Are Met

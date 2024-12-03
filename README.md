# Trading Bot Project

This project is a trading bot that uses various trading strategies to make buy and sell decisions based on cryptocurrency data with multiple ML techniques. It is designed to enhance design pattern usage, implementing **Observer, Strategy, Template Method, and Singleton** patterns to create a modular, maintainable, and extensible architecture.

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

## Screenshots

![WhatsApp Görsel 2024-12-04 saat 00 06 29_fc801c48](https://github.com/user-attachments/assets/987695bc-64c1-40b4-8d53-46c4e4f4e0d9)

![WhatsApp Görsel 2024-12-04 saat 00 06 53_aea1de3c](https://github.com/user-attachments/assets/189a05a5-a491-4f64-931c-75c725f28726)

![WhatsApp Görsel 2024-12-04 saat 00 12 23_a721482c](https://github.com/user-attachments/assets/79c74cba-9f8d-44ed-a710-99be3f27f24e)

![WhatsApp Görsel 2024-12-04 saat 00 08 11_4f2a7641](https://github.com/user-attachments/assets/029a60f6-c5e9-4821-ac3f-e31e9e8f7123)





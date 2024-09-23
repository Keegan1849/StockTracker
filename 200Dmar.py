import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

def track_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period='1d')
        current_price = data['Close'].iloc[-1]
        return float(current_price)
    except Exception as e:
        print(f"Error occurred while fetching data for {symbol}: {e}")
        return None

def track_stock_price_MA(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period='200d')
        moving_average = data['Close'].rolling(window=200).mean()
        return moving_average.iloc[-1]
    except Exception as e:
        print(f"Error occurred while fetching MA data for {symbol}: {e}")
        return None

# Define a list of stock symbols you want to track
stock_symbols = ['PANW', 'NVDA', 'GOOGL', 'MCO', 'CRM', 'HD', 'UNP', 'MSFT', 'COST', 'MA', 'SBUX', 'DGRO', 'UFPI', 'INTU', 'RKLB', 'AAPL']
difference = []

for stock_ticker in stock_symbols:
    price = track_stock_price(stock_ticker)
    ma_price = track_stock_price_MA(stock_ticker)
    
    if price is not None and ma_price is not None:  # Check for price and MA
        difference.append(((price - ma_price) / ma_price) * 100)

# Combine stock symbols and differences, then sort by differences
sorted_data = sorted(zip(stock_symbols, difference), key=lambda x: x[1])

# Unpack sorted data
stock_symbols_sorted, difference_sorted = zip(*sorted_data)

# Create an array of x-positions for the bars
x = np.arange(len(stock_symbols_sorted))  # Use sorted stock symbols for x-axis positions

# Plotting the differences
colors = ['green' if diff > 0 else 'red' for diff in difference_sorted]
bars = plt.bar(x, difference_sorted, color=colors)

# Adding a horizontal line at y = 0
plt.axhline(y=0, color='black', linestyle='--')

# Adding gridlines
plt.grid(axis='y', linestyle='--', color='black')

# Adding data labels with percentage sign
for i, bar in enumerate(bars):
    diff = difference_sorted[i]
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{diff:.2f}%', ha='center', va='bottom', fontsize=8)

# Adding current stock price below x-axis label
stock_prices = [track_stock_price(symbol) for symbol in stock_symbols_sorted]
plt.xticks(x, [f'{symbol}\n${price:.2f}' for symbol, price in zip(stock_symbols_sorted, stock_prices)], fontsize=8)
plt.ylabel('Price / 200-day MA (%)')
plt.title('Price to 200-day Moving Average Ratio')

plt.tight_layout()  # Adjust layout to prevent overlapping labels
plt.show()

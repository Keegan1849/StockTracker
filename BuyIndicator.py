import yfinance as yf
import matplotlib.pyplot as plt
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

def track_stock_50_MA(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period='50d')
        moving_average = data['Close'].rolling(window=50).mean()
        return moving_average.iloc[-1]
    except Exception as e:
        print(f"Error occurred while fetching MA data for {symbol}: {e}")
        return None

def track_stock_15_MA(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period='15d')
        moving_average = data['Close'].rolling(window=15).mean()  
        return moving_average.iloc[-1]
    except Exception as e:
        print(f"Error occurred while fetching MA data for {symbol}: {e}")
        return None

def standard_dev(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period='100d')
        std_dev = data['Close'].rolling(window=100).std().dropna()
        return std_dev.iloc[-1] if not std_dev.empty else None
    except Exception as e:
        print(f"Error occurred while fetching std dev data for {symbol}: {e}")
        return None

# Define a list of stock symbols you want to track
stock_symbols = ['PANW', 'NVDA', 'GOOGL', 'MCO', 'CRM', 'HD', 'UNP', 'MSFT', 'COST', 'MA', 'SBUX', 'DGRO', 'UFPI', 'INTU', 'RKLB', 'AAPL']
Buy = []  # List of stocks with MA difference > 0
std_devs = []  # List to store standard deviations of stocks to be plotted

# Track moving averages and collect buy signals
for symbol in stock_symbols:
    ma_5 = track_stock_15_MA(symbol)
    ma_20 = track_stock_50_MA(symbol)

    if ma_5 is not None and ma_20 is not None:
        Difference = ma_20 - ma_5
        if Difference > 0:
            Buy.append(symbol)  # Append stock symbol if condition is met
            std = standard_dev(symbol)
            std_devs.append(std)  # Collect standard deviations

# Print the list of stocks where MA_20 > MA_5 (Buy signals)
print(f"Stocks with Buy signal: {Buy}")

# Prepare data for y-axis labels
if Buy and std_devs:
    y_labels = [f"Price: {track_stock_price(symbol):.2f}\nStd Dev: {std:.2f}" for symbol, std in zip(Buy, std_devs)]

    # Plotting the bars
    x = np.array(Buy)  # Stock symbols
    y = np.array(std_devs)  # Corresponding standard deviations
    colors = ['green' if val < 5 else 'yellow' if 5 <= val < 10 else 'orange' if 10 <= val < 15 else 'red' if 15 <= val < 20 else 'darkred' for val in y]

    plt.bar(x, y, color=colors, width=0.5)
    plt.grid(axis='y', linestyle='--', color='black')
    plt.axhline(y=0, color='black', linestyle='--')
    plt.xlabel('Stocks')
    plt.ylabel('100-day Standard Deviation')
    plt.title('Standard Deviations of Selected Stocks with Buy Signal')
    plt.xticks(rotation=45)

    # Annotate values with price and standard deviation
    for index, (value, label) in enumerate(zip(y, y_labels)):
        plt.text(index, value, label, ha='center', va='bottom', fontsize=9, bbox=dict(facecolor='white', alpha=0.5))

    plt.show()
else:
    print("No stocks with buy signals or standard deviations to plot.")

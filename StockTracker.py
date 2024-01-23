# Import necessary libraries
from bs4 import BeautifulSoup
import requests
import schedule
import time as tm
import matplotlib.pyplot as plt
import statistics
import _mysql_connector


class StockAnalyzer:
    def __init__(self):
        # Dictionary to store stock data {symbol: [prices]}
        self.stock_data = {}

    # Function to scrape stock prices from a webpage for a given stock symbol
    def scrape_stock_prices(self, symbol):
        try:
            # Scrap the page for the stock price
            url = f"https://search.yahoo.com/search?fr=mcafee&type=E211US885G0&p={symbol}"
            page_to_scrape = requests.get(url)

            # Check if the request was successful (status code 200)
            if page_to_scrape.status_code == 200:
                soup = BeautifulSoup(page_to_scrape.text, "html.parser")

                # Extract stock prices and symbols from the HTML
                prices = soup.findAll("div", attrs={"class": "fin_quotePrice s-price"})

                # Adds stock prices to the dictionary
                self.stock_data.setdefault(symbol, []).clear()
                for price in prices:
                    stock_price = float(price.text.replace(',', ''))
                    self.stock_data[symbol].append(stock_price)

                    # Print stock symbol and price
                    print(f"The stock symbol is {symbol}, and the price is {price.text}")

        except requests.RequestException as e:
            # Handle request exceptions
            print(f"Error accessing the webpage for {symbol}: {e}")

    # Function to calculate the average stock price for a given symbol
# Function to calculate the average stock price for a given symbol
    def calculate_average(self, symbol):
        prices = self.stock_data.get(symbol, [])
        
        if not prices:
            # Handle the case when there are no prices available
            print(f"No prices available for {symbol}")
            return None  # or return some default value or raise an exception
        average_price = statistics.mean(prices)
        print(f'The average stock price for {symbol} is {average_price}')
        return average_price


    # Function to plot a chart of stock prices over time for a given symbol
    def plot_stock_chart(self, symbol):
        fig, ax = plt.subplots()
        ax.plot(self.stock_data.get(symbol, []))

        # Set chart properties
        ax.set_title(f'Stock Prices for {symbol} Over Time')
        ax.set_xlabel('Time (Every 5 seconds)')
        ax.set_ylabel('Stock Price')
        ax.tick_params(labelsize=14)
        ax.grid(True)  # Add grid lines for better readability

        # Display the plot
        plt.show()
class db_connection:
    def __init__(self) -> None:
        pass

# Create an instance of the StockAnalyzer class
stock_analyzer = StockAnalyzer()

# Define a list of stock symbols you want to track
stock_symbols = ['AAPL', 'PLTR', 'MSFT']



# Schedule the job to run every 5 seconds for each stock symbol
for symbol in stock_symbols:
    schedule.every(5).seconds.do(stock_analyzer.scrape_stock_prices, symbol)

# Schedule the stock chart function to run every 5 minutes for each stock symbol
for symbol in stock_symbols:
    schedule.every(5).minutes.do(stock_analyzer.plot_stock_chart, symbol)

# Schedule the average function to run every minute for each stock symbol
for symbol in stock_symbols:
    schedule.every(1).minutes.do(stock_analyzer.calculate_average, symbol)

# Run the scheduled tasks in an infinite loop
while True:
    schedule.run_pending()
    tm.sleep(5)

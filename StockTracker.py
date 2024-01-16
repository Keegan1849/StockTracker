# Import necessary libraries
from bs4 import BeautifulSoup
import requests
import schedule
import time as tm
import matplotlib.pyplot as plt

# List to store stock prices
StockPrices = []

# Function to scrape stock prices from a webpage
def job():
    try:
        # Scrap the page for the stock price
        pageToScrape = requests.get("https://search.yahoo.com/search?fr=mcafee&type=E211US885G0&p=pltr")
        
        # Check if the request was successful (status code 200)
        if pageToScrape.status_code == 200:
            soup = BeautifulSoup(pageToScrape.text, "html.parser")
            
            # Extract stock prices and symbols from the HTML
            prices = soup.findAll("div", attrs={"class": "fin_quotePrice s-price"})
            symbols = soup.findAll("span", attrs={"class": "s-sublabel"})

            # Adds stock price to the list
            for price, symbol in zip(prices, symbols):
                stock_price = float(price.text.replace(',', ''))
                StockPrices.append(stock_price)

                # Print stock symbol and price
                print(f"The stock symbol is {symbol.text.strip()}, and the price is {price.text}")

    except requests.RequestException as e:
        # Handle request exceptions
        print(f"Error accessing the webpage: {e}")

# Function to plot a chart of stock prices over time
def stock_chart():
    fig, ax = plt.subplots()
    ax.plot(StockPrices)
    
    # Set chart properties
    ax.set_title('Stock Prices Over Time')
    ax.set_xlabel('Time (Every 5 seconds)')
    ax.set_ylabel('Stock Price')
    ax.tick_params(labelsize=14)
    ax.grid(True)  # Add grid lines for better readability
    
    # Display the plot
    plt.show()

# Schedule the job to run every 5 seconds
schedule.every(5).seconds.do(job)

# Schedule the stock chart function to run every 5 minutes
schedule.every(5).minutes.do(stock_chart)

# Run the scheduled tasks in an infinite loop
while True:
    schedule.run_pending()
    tm.sleep(5)

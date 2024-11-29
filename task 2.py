import requests
import json

# API Key for Alpha Vantage (replace with your own API key)
API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY'
BASE_URL = 'https://www.alphavantage.co/query'

# Function to get real-time stock price
def get_stock_price(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if 'Time Series (1min)' not in data:
        print(f"Error: Unable to retrieve data for {symbol}.")
        return None

    latest_data = list(data['Time Series (1min)'].values())[0]
    return float(latest_data['1. open'])

# Function to display the portfolio
def display_portfolio(portfolio):
    if not portfolio:
        print("Your portfolio is empty.")
    else:
        print("\nYour Stock Portfolio:")
        for symbol, details in portfolio.items():
            print(f"{symbol}: {details['shares']} shares at ${details['price_per_share']:.2f} each.")

# Function to add a stock to the portfolio
def add_stock(portfolio):
    symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()
    shares = int(input("Enter the number of shares: "))
    
    if symbol in portfolio:
        print(f"{symbol} is already in your portfolio.")
    else:
        price_per_share = get_stock_price(symbol)
        if price_per_share is not None:
            portfolio[symbol] = {
                'shares': shares,
                'price_per_share': price_per_share
            }
            print(f"{symbol} added to your portfolio at ${price_per_share:.2f} per share.")
        else:
            print("Failed to add stock due to an error in retrieving data.")

# Function to remove a stock from the portfolio
def remove_stock(portfolio):
    symbol = input("Enter the stock symbol to remove: ").upper()
    if symbol in portfolio:
        del portfolio[symbol]
        print(f"{symbol} removed from your portfolio.")
    else:
        print(f"{symbol} is not in your portfolio.")

# Function to track the portfolio value
def track_portfolio(portfolio):
    total_value = 0.0
    for symbol, details in portfolio.items():
        current_price = get_stock_price(symbol)
        if current_price is not None:
            total_value += current_price * details['shares']
            print(f"{symbol}: Current price ${current_price:.2f}, Total value ${current_price * details['shares']:.2f}")
        else:
            print(f"Unable to fetch data for {symbol}.")
    
    print(f"\nTotal Portfolio Value: ${total_value:.2f}")

# Main function to run the stock portfolio tracker
def main():
    portfolio = {}
    
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add stock")
        print("2. Remove stock")
        print("3. Display portfolio")
        print("4. Track portfolio value")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            add_stock(portfolio)
        elif choice == '2':
            remove_stock(portfolio)
        elif choice == '3':
            display_portfolio(portfolio)
        elif choice == '4':
            track_portfolio(portfolio)
        elif choice == '5':
            print("Exiting the portfolio tracker.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


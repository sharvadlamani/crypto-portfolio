
import requests

def get_crypto_price(ids, vs_currencies):
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': ','.join(ids),
        'vs_currencies': ','.join(vs_currencies)
    }
    response = requests.get(url, params=params)
    return response.json()

# Example usage
ids = ['bitcoin', 'ethereum']  # List of cryptocurrency ids
vs_currencies = ['usd']        # List of currencies to compare against
prices = get_crypto_price(ids, vs_currencies)
print(prices)

import requests

def get_all_crypto_prices():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',  # Specify the fiat currency
        'order': 'market_cap_desc',  # Sort by market cap
        'per_page': 100,  # Number of results per page (max 250)
        'page': 1  # Page number
    }
    response = requests.get(url, params=params)
    return response.json()

# Example usage
prices = get_all_crypto_prices()
for crypto in prices:
    print(f"Name: {crypto['name']}, Symbol: {crypto['symbol']}, Price: {crypto['current_price']}")


print(prices[0])
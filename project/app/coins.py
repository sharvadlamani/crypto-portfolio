#get list of all the coins
from .models import Coin
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

def get_crypto_details():
    prices = get_all_crypto_prices()
    coins=[]
    for crypto in prices:
        if type(crypto)!=dict:
            continue
        coin={
            "name" :crypto['name'],
            "symbol" :crypto['symbol'],
            "price" :float(crypto['current_price']),
            "change24hrpercentage": float(crypto['price_change_percentage_24h'])}
        coins.append(coin)
    return coins


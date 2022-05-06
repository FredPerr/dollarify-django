import requests

from dollarify.settings import ALPHA_VANTAGE_API_KEY


CURRENCIES = (
    ('CAD', 'CAD'),
    ('USD', 'USD')
)


def get_conversion_rate(from_cur, to_cur):
    if from_cur == to_cur:
        return 1.0
    
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_cur}&to_currency={to_cur}&apikey={ALPHA_VANTAGE_API_KEY}"
    r = requests.get(url)
    data = r.json()
    rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    return rate
# currency_converter.py
import requests

API_KEY = 'fcd9183095209ffc8df4404f31d4b75d'  # Replace with your actual CurrencyLayer API key
BASE_URL = 'http://api.currencylayer.com/'

def get_exchange_rates():
    """Fetch live exchange rates from CurrencyLayer."""
    url = f'{BASE_URL}live?access_key={API_KEY}&currencies=EUR,GBP,CAD,PLN&source=USD&format=1'
    try:
        response = requests.get(url)
        data = response.json()
        print(data)  # Add this line to debug the response
        if data.get('success'):
            return data['quotes']
        else:
            error_info = data.get('error', {})
            error_code = error_info.get('code', 'Unknown')
            error_message = error_info.get('info', 'No error message provided')
            print(f"API Request Error: {error_code} - {error_message}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def convert_currency(from_currency, to_currency, amount):
    """Convert currency using the fetched exchange rates."""
    rates = get_exchange_rates()
    if not rates:
        print("Failed to fetch exchange rates.")
        return None

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    # Handle USD conversions separately
    if from_currency == 'USD':
        from_rate = 1.0
    else:
        from_currency_key = f'USD{from_currency}'
        if from_currency_key not in rates:
            print(f"Currency not found: {from_currency}")
            return None
        from_rate = rates[from_currency_key]

    if to_currency == 'USD':
        to_rate = 1.0
    else:
        to_currency_key = f'USD{to_currency}'
        if to_currency_key not in rates:
            print(f"Currency not found: {to_currency}")
            return None
        to_rate = rates[to_currency_key]

    # Conversion formula: amount * (to_rate / from_rate)
    converted_amount = (amount / from_rate) * to_rate
    return round(converted_amount, 2)

# Example usage
amount_in_eur = 100
converted_amount = convert_currency('EUR', 'GBP', amount_in_eur)
if converted_amount is not None:
    print(f"{amount_in_eur} EUR is equal to {converted_amount} GBP")
from datetime import date

class Constants:
    API_KEY = '848c671e59317734aa9eb0226d7af248'
    COLUMNS_BOVESPA = ['Close']
    END_DATE = date.today().strftime('%Y-%m-%d')
    STOCK_SYMBOL = '^BVSP'
    START_DATE = '1994-01-01'
    FED_URL = 'https://api.stlouisfed.org/fred/'
    FED_OBSERVATION_ENDPOINT = 'series/observations'


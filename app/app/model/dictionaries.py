from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')

class Dictionaries:
    EFFECTIVE_FEDERAL_FUNDS_RATE = {
    'series_id': 'EFFR',
    'api_key': '848c671e59317734aa9eb0226d7af248',
    'file_type': 'json',
    'observation_start': '2000-07-03',
    'observation_end': today,
    'ts_frequency': 'm',
    }
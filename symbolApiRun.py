from symbolApiFunctions import *

import json
import requests
import config as c
from datetime import date, datetime, timedelta
from requests.exceptions import HTTPError
from time import perf_counter


t1_start = perf_counter()
apikey = c.api_key()

symbol_url = "https://eodhistoricaldata.com/api/exchanges/US"
symbol_params = {
    'api_token': apikey,
    'fmt': 'json'
}


def run(URL, PARAMS):

    response = api_request(URL, PARAMS)
    response_nasdaq = nasdaq_only(response)

    # response_nasdaq_example = [{"Code":"ZXZZT","Name":"NASDAQ TEST STOCK","Country":"USA","Exchange":"NASDAQ","Currency":"USD","Type":"Common Stock"}, {"Code":"ZZT","Name":"TEST STOCK","Country":"USA","Exchange":"NASDAQ","Currency":"USD","Type":"Common Stock"}]

    connect_db(response_nasdaq)


run(symbol_url, symbol_params)

t1_stop = perf_counter()
print(t1_stop-t1_start, "seconds")

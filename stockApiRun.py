from stockApiFunctions import *
import config as c
import json
import requests
from datetime import date, datetime, timedelta
from requests.exceptions import HTTPError
from time import perf_counter


t1_start = perf_counter() 
apikey = c.api_key()


def run():

    conn = connect_DB()
    # symbol_table='symbolTable'
    tickers = get_ticker_list(conn)

    for ticker in tickers:
        json_data = api_request(ticker)
        cur = conn.cursor()

        insert_ticker_data(conn, cur, ticker, json_data)

    conn.commit()
    conn.close()


run()

t1_stop = perf_counter() 
print(t1_stop-t1_start, "seconds")

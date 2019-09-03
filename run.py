from download import get_api_data, insert_data_db
from datetime import datetime, date
import config as c
import json
from time import perf_counter


# start_time = time.clock()
t1_start = perf_counter()  

# file='tickers.txt'
file = 'forTestTickers.txt'
# tickers = ['AAPL']

def get_tickers(file):
    with open(file, 'r') as filehandle:
        basicList = json.load(filehandle)
        print(len(basicList))
        return basicList

tickers = get_tickers(file)


start = "2019-08-30"
end = str(date.today())
apikey = c.get_keys()
freq='d'

eod_params = { 'from':start,'to':end,'api_token':apikey,'period':freq,'fmt':'json'} 

def add_to_db(tickers,params):

        for ticker in tickers:
                eod_url= f"https://eodhistoricaldata.com/api/eod/{ticker}.US"
                
                json_response = get_api_data(eod_url, params)

                for i in json_response:
                         i.update({'ticker':ticker})

                print(json_response)
                insert_data_db(i)

add_to_db(tickers,eod_params)

t1_stop = perf_counter() 
print(t1_start-t1_stop, "seconds")
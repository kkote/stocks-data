
from datetime import datetime
import config as c
import json
import requests
from requests.exceptions import HTTPError

def constructEODurl(ticker,start_date,end_date,freq):

    start=datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    start = str(start_date)
    end = str(end_date)    
    apikey = c.get_keys()

    EODurl= f"https://eodhistoricaldata.com/api/eod/{ticker}.US?from={start}&to={end}&api_token={apikey}&period={freq}&fmt=json"
    #  EODurl= f"https://eodhistoricaldata.com/api/eod/{ticker}.US?to={end}&api_token={apikey}&period=m&fmt=json"
   
    return EODurl


def download(filePath,urlOfFile):
    # import requests
    # from requests.exceptions import HTTPError

    print(urlOfFile)
    
    # response = requests.get(urlOfFile)
    # json_response = response.json()
    json_response=[{'date': '2019-08-05', 'open': 2, 'high': 21, 'low': 20, 'close': 208, 'adjusted_close': 207, 'volume': 54}, {'date': '2019-08-06', 'open': 205.53, 'high': 206.43, 'low': 201.63, 'close': 204.02, 'adjusted_close': 203.2478, 'volume': 38688200}]

    print(json_response)
    return json_response

    # print(json_response)


def insertIntoDB(api_data):
    import mysql.connector
    from datetime import date, datetime, timedelta

    mydb = mysql.connector.connect(
        database='test'
    )

    cur = mydb.cursor()

    insert_ticker = ("INSERT INTO testTable "
                    "(ticker,date, open,high,low, close, adjusted_close,volume) "
                    "VALUES (%(ticker)s, %(date)s, %(open)s, %(high)s, %(low)s, %(close)s, %(adjusted_close)s, %(volume)s)")
    # the_date = datetime(2019, 8, 1)
    cur.execute(insert_ticker, api_data)

    emp_no = cur.lastrowid

    mydb.commit()
    cur.close()
    mydb.close()
import config as c
import json
import requests
from requests.exceptions import HTTPError
from datetime import date, datetime, timedelta



def get_ticker_list(conn):
    symbol_table=c.symbols_t()
    cur = conn.cursor()
    query = f"SELECT `code` FROM {symbol_table}"
    cur.execute(query)
    ticker_list = [item[0] for item in cur.fetchall()]
    cur.close()
    return(ticker_list)



def connect_DB():
    import mysql.connector
    from mysql.connector import errorcode, Error

    # conn = mysql.connector.connect(
    #         database = c.db_name(),
    #         user=c.db_user(),
    #         host=c.db_host(),
    #         password=c.db_password()  
    # )
    # print(f"print conn: {conn}")
    # return(conn)

     try:
        connection = mysql.connector.connect(
            database = c.db_name(),
            user=c.db_user(),
            host=c.db_host(),
            password=c.db_password()
        )

        print(f"print conn: {connection}")

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)

        return(connection)

    except Error as e:
        print("Error while connecting to MySQL", e)



def api_request(ticker):
    apikey = c.api_key()
    start=str('2019-09-26')
    end = str(date.today())

    URL = f"https://eodhistoricaldata.com/api/eod/{ticker}.US"
    PARAMS = {'start': start,'to':end,'api_token':apikey,'period':'d','fmt':'json'}

    r = requests.get(url = URL, params = PARAMS) 
    data = r.json() 
    for i in data:
        i.update({'ticker':ticker})
    return data


def insert_ticker_data(conn, cur, ticker, json_data):


    insert_row = ("INSERT INTO nasdaq_table (date,  open,high,low, close, adjusted_close,volume, ticker) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

    # value_list = list(json_data.values())
    # cur.executemany(insert_row, json_data)
    
    for i in json_data:
        value_list = list(i.values())
        cur.execute(insert_row,value_list)
 
    conn.commit()
    cur.close()



# def get_values(ticker_json):
#     values = ", ".join(["%s"] * len(ticker_json))
#     columns=",".join(ticker_json.keys())
#     value_list = list(ticker_json.values())
#     return value_list, insert_row
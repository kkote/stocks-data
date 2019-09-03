
import json
import requests
import json
import config as c
from datetime import date, datetime, timedelta
from requests.exceptions import HTTPError



def get_api_data(URL, PARAMS):

    r = requests.get(url = URL, params = PARAMS) 
    data = r.json() 

    return data


def insert_data_db(api_data):
    import mysql.connector
    from mysql.connector import errorcode, Error

    pwd = c.db_password()
    db = '******'
    user='****'
    host='*****'
    
    insert_row = ("INSERT INTO tableS "
                    "(ticker,date, open,high,low, close, adjusted_close,volume) "
                    "VALUES (%(ticker)s, %(date)s, %(open)s, %(high)s, %(low)s, %(close)s, %(adjusted_close)s, %(volume)s)")

    try:
        conn = mysql.connector.connect(
            database = db,
            user=user,
            host=host,
            password=pwd
        )

        cur = conn.cursor()
        cur.executemany(insert_row,api_data)
        conn.commit()

    except Error as error:
      print(error)
    
    finally:
      cur.close()
      conn.close()
import json
import requests
import config as c
from requests.exceptions import HTTPError


def api_request(URL, PARAMS):
    r = requests.get(url = URL, params = PARAMS) 
    data = r.json() 
    return data

def nasdaq_only(response):
     only_nasdaq_rows = [x for x in response if x['Exchange'] == 'NASDAQ']
    #  print(len(only_nasdaq))
     return(only_nasdaq_rows)
 

def connect_db(response_nasdaq):
    import mysql.connector

    table_name='testSymbol'
    pwd = c.db_password()
    db='test'

    conn = mysql.connector.connect(
            database = db,
            user='kate',
            host='localhost',
            password=pwd
        )
    
    cur = conn.cursor()
    

    cur.execute("CREATE TABLE symbols_info (	`code` VARCHAR(10),`name` VARCHAR(50),`country` VARCHAR(15),`exchange` VARCHAR(10),`currency` VARCHAR(10),`type` VARCHAR(20),`id` INT NOT NULL AUTO_INCREMENT)")
    # mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")

    for i in response_nasdaq:
        values = ", ".join(["%s"] * len(i))
        # columns=",".join(i.keys())
        # insert_query = f"insert into {table_name} ({columns}) values ({values});"
        value_list = list(i.values())

        cur.execute("INSERT INTO symbols_info  (code, name, country, exchange, currency, type) VALUES (%s,%s,%s,%s,%s,%s)", (value_list))
        # cur.execute("INSERT INTO testSymbol  (code, name, country, exchange, currency, type) VALUES (%s,%s,%s,%s,%s,%s)", (value_list))


    conn.commit()
    cur.close()
    conn.close()

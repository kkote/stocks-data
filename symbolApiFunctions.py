import json
import requests
import config as c
from requests.exceptions import HTTPError


def api_request(URL, PARAMS):
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    return data


def nasdaq_only(response):
    only_nasdaq_rows = [x for x in response if x['Exchange'] == 'NASDAQ']
    return(only_nasdaq_rows)


def connect_db(response_nasdaq):
    import mysql.connector

    table = c.db_tickers_table()
    pwd = c.db_password()
    user = c.db_user()
    host = c.db_host()
    db = c.db_database()

    conn = mysql.connector.connect(
        database=db,
        user=user,
        host=host,
        password=pwd
    )

    cur = conn.cursor()

    cur.execute(f"CREATE TABLE {table} (	`code` VARCHAR(10),`name` VARCHAR(50),`country` VARCHAR(15),`exchange` VARCHAR(10),`currency` VARCHAR(10),`type` VARCHAR(20),`id` INT NOT NULL AUTO_INCREMENT)")

    for i in response_nasdaq:
        values = ", ".join(["%s"] * len(i))
        # columns=",".join(i.keys())
        # insert_query = f"insert into {table_name} ({columns}) values ({values});"
        value_list = list(i.values())

        cur.execute(
            f"INSERT INTO {table}  (code, name, country, exchange, currency, type) VALUES (%s,%s,%s,%s,%s,%s)", (value_list))

    conn.commit()
    cur.close()
    conn.close()

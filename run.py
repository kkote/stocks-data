from download import constructEODurl
from download import download
from download import insertIntoDB
import json


# file='tickers.txt'
file='forTestTickers.txt'

def tickerLength(file):
    with open(file, 'r') as filehandle:
        basicList = json.load(filehandle)
        print(len(basicList))
        return basicList

tickers=tickerLength(file)


start_date = "2019-08-01"
end_date = "2019-08-03"
freq = "d"
# frequency d = daily, w= weekly, m=monthly


for ticker in tickers:
    # print(ticker)
    localFilePath="CSV/theTestLoop.txt"
    EodUrl = constructEODurl(ticker,start_date,end_date,freq)

    json_response = download(localFilePath,EodUrl)

    for i in json_response:
        i.update({'ticker':ticker})
        insertIntoDB(i)

from datetime import datetime
from sqlite3 import Timestamp
import urllib.parse
import hashlib
import hmac
import base64
import time
import os
import requests
import datetime



from dotenv import load_dotenv

load_dotenv()


buy_price = 0
sell_price = 0
first_time = 0


# Read Kraken API key and secret stored in environment variables
api_url = "https://api.kraken.com"
api_key = os.getenv('API_KEY_KRAKEN')
api_sec = os.getenv('API_SEC_KRAKEN')

def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


# Attaches auth headers and returns results of a POST request
def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)             
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req

# BOT Functions
def server_time():
    resp = requests.get('https://api.kraken.com/0/public/Time')
    data = resp.json().get('result')
    time_now = data.get('unixtime')
    return time_now 

def get_btc_balance(api_key, api_sec):
    # Construct the request and print the result
    resp = kraken_request('/0/private/Balance', {
        "nonce": str(int(1000*time.time()))
    }, api_key, api_sec)
    data = resp.json().get('result')
    return data.get('XXBT')

def get_usdt_balance(api_key, api_sec):
    # Construct the request and print the result
    resp = kraken_request('/0/private/Balance', {
        "nonce": str(int(1000*time.time()))
    }, api_key, api_sec)
    data = resp.json().get('result')
    return data.get('USDT')

def get_price_BTC():
    resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTUSDT')
    data = resp.json().get('result')
    prices = data.get('XBTUSDT')
    price = prices.get('a')
    return price[0]

def get_volume_BTC():
    resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTUSDT')
    data = resp.json().get('result')
    volumes = data.get('XBTUSDT')
    volume = volumes.get('v')
    return volume[0]

def get_triller_volume_BTC_10mins():
    time_now = server_time()
    time_now = time_now - 600
    resp = requests.get('https://api.kraken.com/0/public/OHLC?pair=XBTUSDT&interval=1&since='+str(time_now))
    data = resp.json().get('result')
    volumes = data.get('XBTUSDT')
    y=0
    x=1;
    mins = []
    volume = []
    triller_volume = 0.0

    while x <= 9:
        volume.append(volumes[x][6])
        mins.append(volumes[x][0])    
        triller_volume = triller_volume + float(volume[y])
        y = y + 1
        x = x + 1
    return round(triller_volume/10,2)

def get_volume_by_mins(priceBTC):
    time_now = server_time()
    time_now = time_now - 60
    #print(datetime.datetime.fromtimestamp(time_now))
    resp = requests.get('https://api.kraken.com/0/public/OHLC?pair=XBTUSDT&interval=1&since='+str(time_now))
    data = resp.json().get('result')
    volumes = data.get('XBTUSDT')
    
    return round(float(volumes[0][6])*priceBTC,2)


def test_operation(priceBTC,counter, balance):
    global first_time, sell_price, buy_price
    print("INFO---------")
    print("Counter: ",counter)
    print("Price BTC: ", priceBTC)
    print("Balance: ", balance)
    if first_time == 0:
        print("COMPRA en el", priceBTC)
        buy_price = priceBTC
        balance_average = 0
        first_time = 1
    else:
        if counter%2 == 0:
            print("COMPRA en el", priceBTC)
            balance_average = ((sell_price-priceBTC)/sell_price)*100
            print("Average: ",round(balance_average,2),"%")
            
            buy_price = priceBTC
        else:
            print("VENTA en el", priceBTC)
            balance_average = -((buy_price-priceBTC)/buy_price)*100
            print("Average: ",round(balance_average,2),"%")
            
            sell_price = priceBTC
    
    balance = balance + ((balance*balance_average)/100)
    print("Final Balance: ",round(balance,2))
    time.sleep(60)
    return balance





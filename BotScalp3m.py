import time
import os
import requests
from dotenv import load_dotenv
import urllib.parse
import hashlib
import hmac
import base64
import datetime

load_dotenv()

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
    resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTUSD')
    data = resp.json().get('result')
    prices = data.get('XXBTZUSD')
    price = prices.get('a')
    return price[0]

def get_volume_BTC():
    resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTUSD')
    data = resp.json().get('result')
    volumes = data.get('XXBTZUSD')
    volume = volumes.get('v')
    return volume[0]

def get_triller_volume_BTC_10days():
    time_now = server_time()
    time_now = time_now - 950400
    resp = requests.get('https://api.kraken.com/0/public/OHLC?pair=XBTUSD&interval=1440&since='+str(time_now))
    data = resp.json().get('result')
    volumes = data.get('XXBTZUSD')
    y=0
    x=1;
    days = []
    volume = []
    triller_volume = 0.0;
    
    while x <= 10:
        volume.append(volumes[x][6])
        days.append(volumes[x][0])
        times = datetime.datetime.fromtimestamp(days[y])
        triller_volume = triller_volume + float(volume[y])
        y = y + 1
        x = x + 1
    return round(triller_volume/10,2)
   
 
    
#SHOW DATA
def show_data():
    btc_balance = float(get_btc_balance(api_key, api_sec))
    usdt_balance = float(get_usdt_balance(api_key, api_sec))
    price_btc = float(get_price_BTC())
    volume_btc = float(get_volume_BTC())
    print("\n\n")
    print("-USER & BTCUSD DATA-")
    print("____________________\n\n")

    print("BTC Balance: ",round(btc_balance,2))
    print("USDT Balance: ",round(usdt_balance,2))
    print("BTC price: ", round(price_btc,2))
    print("BTC volume: ", round(volume_btc,2))
    print("BTC Climatic Vol: ", get_triller_volume_BTC_10days())
    print("\n\n")



#MAIN
show_data()




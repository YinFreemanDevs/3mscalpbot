from .data_functoins import *

usdt_balance_init = 5000
final_balance = 5000
counter = 0

#SHOW DATA
def show_data():
    
    btc_balance = float(get_btc_balance(api_key, api_sec))
    usdt_balance = float(get_usdt_balance(api_key, api_sec))
    price_btc = float(get_price_BTC())
    volume_btc = float(get_volume_BTC())
    vol_last = get_volume_by_mins(price_btc)
    
    if(vol_last > 100000):
        print("\n\n")
        print("-USER & BTCUSD DATA-")
        print("____________________\n\n")
        print("BTC Balance: ",round(btc_balance,2))
        print("USDT Balance: ",round(usdt_balance,2))
        print("BTC price: ", round(price_btc,2))
        print("BTC volume: ", round(volume_btc*price_btc,2))
        print("BTC Climatic Vol: ", round(get_triller_volume_BTC_10mins(price_btc)*price_btc,2))
        print("Last Volume: ", vol_last )
        print("ALERTA DE COMPRA/VENTA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("\n\n")
        

#SHOW DATA
def show_data_test():
    global usdt_balance_init,final_balance,counter
    price_btc = float(get_price_BTC())
    volume_btc = float(get_volume_BTC())
    vol_last = get_volume_by_mins(price_btc)
   
    if(vol_last > 20000):
        final_balance = test_operation(price_btc, counter, final_balance)
        print("\n\n")
        print("-USER & BTCUSD DATA-")
        print("____________________\n\n")
       
        print("USDT Init Balance: ",usdt_balance_init)
        print("BTC price: ", round(price_btc,2))
        print("BTC volume: ", round(volume_btc*price_btc,2))
        print("BTC Climatic Vol: ", round(get_triller_volume_BTC_10mins()*price_btc,2))
        print("Last Volume: ", vol_last )
        print("Final Balance: ", round(final_balance,2))
        print("\n\n")
        counter = counter + 1
    return round(final_balance,2)

    


#!/bin/python

from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import uniform
import logging
import requests
from datetime import datetime

# Params

host = "127.0.0.1"
port = 5020
api_key = "2df983e16553798e0e90aa3433bce20c"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name_1 = "bucaramanga"
city_name_2 = "puebla"
units="metric"
url_bucaramanga = base_url + "appid=" + api_key + "&q=" + city_name_1 + "&units=" + units
url_puebla = base_url + "appid=" + api_key + "&q=" + city_name_2 + "&units=" + units

# Create an instance of ModbusServer

server = ModbusServer("127.0.0.1", 5020, no_block=True)

FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)



try:
    print("Start server...")
    server.start()
    print("Server is online")
    state = [0]
    while True:
        response_1 = requests.get(url_bucaramanga)
        response_2 = requests.get(url_puebla)
        x = response_1.json()
        y = response_2.json()
        print(x)
        temp_buc=float(x['main']['temp'])*100
        temp_pue=float(y['main']['temp'])*100
        
        server.data_bank.set_holding_registers(0,[temp_buc, temp_pue])
    

        if state != server.data_bank.get_holding_registers(0,2):
            state = server.data_bank.get_holding_registers(0,2)
            print("Value of Registers 1,2 has changed to " +str(state))

        sleep(30)

except:
    print("Shutdown server ...")
    server.stop()
    print("Server is offline")
# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
import machine, gc, wifi
from time import sleep

if not wifi.isconnected():
    connexion = wifi.autoconnect()
    if connexion == -1:
        print('No known network in range...')
        wifi.ap_config()
    elif connexion == 0:
        sleep(5)
        wifi.autoconnect()

gc.collect()

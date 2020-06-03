# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import machine, network, gc, ntptime
from time import sleep
# import uos
# uos.dupterm(None, 1) # disable REPL on UART(0)
import webrepl
webrepl.start()
gc.collect()

import wifi

if not wifi.isconnected():
    connexion = wifi.autoconnect()
    if connexion == -1:
        print('No known network in range')
        wifi.ap_config()
    elif connexion == 0:
        sleep(5)
        wifi.autoconnect()

gc.collect()

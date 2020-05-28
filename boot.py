# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import machine, network, gc, ntptime
# import uos
#uos.dupterm(None, 1) # disable REPL on UART(0)
import webrepl
webrepl.start()
gc.collect()

with open('ssid.conf', 'r') as f:
    data = f.read()

ssid, psswd = data.strip().split(',')

try:
    import usocket as socket
except:
    import socket

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, psswd)
        while not wlan.isconnected():
            pass
    print('network config:', *wlan.ifconfig()[:-1])

connect()

ntptime.settime()

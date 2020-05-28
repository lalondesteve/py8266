# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import machine, network, gc, ntptime
# import uos
# uos.dupterm(None, 1) # disable REPL on UART(0)
import webrepl
webrepl.start()
# gc.collect()

with open('ssid.conf', 'r') as f:
    netdata = f.read().strip().split(',')

try:
    import usocket as socket
except:
    import socket
print(gc.mem_free())
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(*netdata)
        while not wlan.isconnected():
            pass
    print('network config:', *wlan.ifconfig()[:-1])

connect()
ntptime.settime()
# print('post-boot', gc.mem_free())
gc.collect()
# print('post-collect', gc.mem_free())
# gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
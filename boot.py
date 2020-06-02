# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import machine, network, gc, ntptime
# import uos
# uos.dupterm(None, 1) # disable REPL on UART(0)
import webrepl
webrepl.start()
# gc.collect()
import usocket as socket
from time import localtime as lt
# get wifi data from file
with open('ssid.conf', 'r') as f:
    netdata = f.read().strip().split(',')

def connect():
    '''activate and connect to wifi if not connected and print settings'''
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        wlan.active(True)
        wlan.connect(*netdata)
        while not wlan.isconnected():
            pass
    print('network config', wlan.ifconfig())

def now():
    # y, m, d, h, m, s, _, _ = lt()
    return "{0}-{1:=02}-{2:=02}_{3:=02}:{4:=02}:{5:=02} ".format(*lt())

def log_write(data):
    with open('log.log', 'a') as f:
        f.write(now())
        f.write(data)
        f.write('\n')

connect()
ntptime.settime()
log_write('Reboot completed')
gc.collect()
# gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
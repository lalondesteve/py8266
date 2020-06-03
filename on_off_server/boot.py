# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import machine, network, gc, ntptime
from time import sleep
# import uos
# uos.dupterm(None, 1) # disable REPL on UART(0)
# import webrepl
# webrepl.start()
gc.collect()
import usocket as socket
from time import localtime as lt
from time import sleep

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def get_net_conf():
    with open('ssid.conf', 'r') as f:
        data = f.read()
    return data.strip().split(',')
    

def connect():
    attempts = 0
    ssid, psswd = get_net_conf()
    while not wlan.isconnected():
        wlan.connect(ssid, psswd)
        attempts += 1
        sleep(5)
        if attempts > 3:
            break
    sleep(1)
    print('network config:', *wlan.ifconfig()[:-1])
    return wlan.isconnected()

def now():
    # y, m, d, h, m, s, _, _ = lt()
    return "{0}-{1:=02}-{2:=02}_{3:=02}:{4:=02}:{5:=02} ".format(*lt())

def log_write(data):
    with open('log.log', 'a') as f:
        f.write(now())
        f.write(data)
        f.write('\n')

print(connect())

try:
    ntptime.settime()
except: 
    pass
log_write('Reboot completed')
gc.collect()
# gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

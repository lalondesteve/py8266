# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import machine, network, gc, ntptime
# import uos
# uos.dupterm(None, 1) # disable REPL on UART(0)
import webrepl
webrepl.start()
gc.collect()

import wifi

server = wifi.ap_config()
data = server.serve()
print(data)
gc.collect()
data = server.serve()


# wlan = network.WLAN(network.STA_IF)

# with open('ssid.conf', 'r') as f:
#     data = f.read()
#
# ssid, psswd = data.strip().split(',')
#
# try:
#     import usocket as socket
# except:
#     import socket

# def connect():
#     from time import sleep
#     attempts = 0
#     wlan.active(True)
#     if not wlan.isconnected():
#         wlan.connect(ssid, psswd)
#         while not wlan.isconnected():
#             attempts += 1
#             sleep(2)
#             if attempts > 3:
#                 break
#     print('network config:', *wlan.ifconfig()[:-1])
#     return wlan.isconnected()
#
# connect()

#connect()
ntptime.settime()
#log_write('Reboot completed')
gc.collect()
# gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

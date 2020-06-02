import wifi

scan = wifi.scan()
connected = autoconnect(scan, wifi.get_conf())
if connected == -1:
    server = wifi.ap_config()

server.start()
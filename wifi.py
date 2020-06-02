import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
mac = wlan.config('mac')
essid = '8266-'+''.join(['{:02x}'.format(b) for b in mac[3:]])

def scan():
    return [x[0] for x in wlan.scan()]

def get_conf():
    with open('ssid.conf', 'rb') as f: 
        return f.read().split(b'\n')

def add_conf(ssid, psswd):
    with open('ssid.conf', 'ab') as f: 
        f.write(b'\n%b,%b' % (ssid, psswd))

def connect(ssid, psswd):
    from time import sleep
    attempts = 0
    if not wlan.isconnected():
        wlan.connect(ssid, psswd)
        while not wlan.isconnect():
            attempts += 1
            sleep(2)
            if attempts > 3:
                break
    print('network config:', *wlan.ifconfig())
    return wlan.isconnected()

def gen_options(scan):
    data = []
    base = '<option value="_name">_name</option>'
    for name in scan:
        d = base.replace('_name', name)
        data.append(d)
    return ' '.join(data)

def get_portal_page(essid, options):
    gc.collect()
    with open('portal.html', 'rb') as f: 
        return (f.read()
                .replace(b'ap_name', essid.encode('utf8'))
                .replace(b'net_ssid', options.encode('utf8'))
                )

def autoconnect(scan, conf):
    my_net = None
    for n in scan:
        for c in conf:
            if n in c:
                my_net = c
                break
    if my_net:
        connect(my_net[0], my_net[1])
        return wlan.isconnected()
    else:
        return -1

def ap_config():
    from html_server import HTMLServer
    from time import sleep
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=essid, authmode=1)
    ap.active(True)
    ip = ap.ifconfig()[0]
    while ip == '0.0.0.0':
        sleep(1)
        ip = ap.ifconfig()[0]
    return HTMLServer(ap.ifconfig()[0])


def extract_data(response):
    response.split(b'\n')
    ssid = [x.rstrip() for x in response if x.startwith(b'ssid=')][0]
    psswd = [x.rstrip() for x in response if x.startwith(b'psswd=')][0]
    return ssid, psswd



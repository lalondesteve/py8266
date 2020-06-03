import network
from time import sleep

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
sleep(0.1)
mac = wlan.config('mac')
ESSID = 'ESP8266-'+''.join(['{:02x}'.format(b) for b in mac[3:]])

def isconnected():
    return wlan.isconnected()

def _scan():
    return tuple(x[0] for x in wlan.scan())

def get_conf():
    with open('ssid.conf', 'rb') as f: 
        return f.read().split(b'\n')

def add_conf(ssid, psswd):
    if not ssid or not psswd:
        return False
    with open('ssid.conf', 'ab') as f: 
        f.write(b'\n')
        f.write(ssid)
        f.write(b',')
        f.write(psswd)
    return True

def extract_data(response):
    r = response.split(b'\n')
    ssid = [x.rstrip() for x in r if x.startswith(b'ssid=')][0][5:]
    psswd = [x.rstrip() for x in r if x.startswith(b'psswd=')][0][6:]
    return ssid, psswd

def gen_options():
    data = []
    base = b'<option value="_ssid">_ssid</option>'
    for ssid in _scan():
        d = base.replace(b'_ssid', ssid)
        data.append(d)
    return b' '.join(data)

def get_portal_page():
    options = gen_options()
    with open('portal.html', 'rb') as f: 
        return (
                f.read()
                .replace(b'ap_name', ESSID.encode('utf8'))
                .replace(b'scan_ssid', options)
                )

def connect(ssid, psswd):
    wlan.active(False)
    sleep(0.1)
    for _ in range(3):
        if wlan.isconnected():
            break
        print('Attempting connexion', ssid.decode())
        wlan.active(True)
        sleep(0.1)
        wlan.connect(ssid, psswd)
        sleep(5)
    sleep(1)
    print('network config:', *wlan.ifconfig())
    return wlan.isconnected()

def autoconnect():
    scan = _scan()
    conf = get_conf()
    my_net = None
    for n in scan:
        for c in conf:
            if n in c:
                my_net = c.split(b',')
                break
    if my_net:
        return connect(*my_net)
    else:
        return -1

def ap_config():
    from html_server import HTMLServer
    print('Starting configure server')   
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ESSID, authmode=1)
    ip = ap.ifconfig()[0]
    while ip == '0.0.0.0':
        sleep(1)
        ip = ap.ifconfig()[0]
    server = HTMLServer(ap.ifconfig()[0], html_get_func=get_portal_page)
    while True:
        data = server.serve()
        try:
            ssid, psswd = extract_data(data)
            if connect(ssid, psswd):
                print('configuration added:', add_conf(ssid, psswd))
                sleep(1)
                break
        except Exception as e:
            print(e)
    ap.active(False)
    sleep(0.1)

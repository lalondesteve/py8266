from relay import Relay
from time import localtime as lt

r = Relay()

html = ""
with open("pcb2.html", 'r') as f:
    html = f.read()

def web_page():
    if r.get_value():
        r_state = "ON"
    else:
        r_state = "OFF"
    return html.replace('r_state', r_state)

def now():
    # y, m, d, h, m, s, _, _ = lt()
    return "{0}-{1:=02}-{2:=02}_{3:=02}:{4:=02}:{5:=02} ".format(*lt())

def log_write(data):
    with open('log.txt', 'a') as f:
        f.write(now())
        f.write(data)
        f.write('\n')

def serve():
    while True:
        conn, addr = s.accept()
        request = conn.recv(1024)
        command = request.split()[1][4:]
        if command == b'on':
            r.on()
        elif command == b'off':
            r.off()
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
        if not command:
            log_data = 'Connected from: {0} with request: {1}'.format(addr[0], command.decode())
        else:
            log_data = 'Connected from: {0}'.format(addr[0])
        print(log_data)
        log_write(log_data)
        gc.collect()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    serve()
except KeyboardInterrupt:
    log_write(now() + ' KeyboardInterrupt')
    pass
finally:
    log_write(now() +' Closing Socket')
    s.close()
    gc.collect()



    
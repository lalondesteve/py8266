from relay import Relay

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

def serve():
    while True:
        conn, addr = s.accept()
        request = conn.recv(1024)
        if not request:
            continue
        try:
            command = request.split()[1][4:]
        except Exception as e:
            log_data(str(e))
            log_data('Request {0}'.format(request.decode()))
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
        log_data = 'Connected from: {0} with request: {1}'.format(addr[0], request.decode())
        # print(log_data)
        log_write(log_data)
        gc.collect()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    serve()
except KeyboardInterrupt as e:
    log_write(str(e))
    pass
except Exception as e:
    log_write(str(e))
    if 'EADDRINUSE' in str(e):
        machine.reset()
finally:
    log_write('Closing Socket')
    s.close()
    gc.collect()
    


    
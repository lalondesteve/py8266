# -*- coding: utf-8 -*-
try:
    import usocket as socket
except:
    import socket
from time import sleep

class HTMLServer(object):
    def __init__(self, ip, port=80,  html_get_func=None):
        self.ip = ip
        self.port = port
        self.html = html_get_func
        self.s = self.init_socket()
        self.html = html_get_func
        if not self.html:
            self.html = self.get_html
        # self.s.settimeout(5)

    def init_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip, self.port))
        s.listen(5)
        return s

    def serve(self):
        # gc.collect()
        if not self.s:
            self.s = self.init_socket()
        print('Server started at', self.ip, self.port)
        while True:
            process = False
            conn, addr = self.s.accept()
            request = conn.recv(8192)
            print(request)
            if request.split()[0] == b'POST':
                request = request
                response = self.processing_html()
                process = True
            else:
                response = self.html()
            conn.send(b'HTTP/1.1 200 OK\n')
            conn.send(b'Content-Type: text/html; charset=utf-8\n\n')
            conn.send(b'Connection: close\n\n')
            conn.sendall(response.encode('utf8'))
            conn.close()
            sleep(.1)
            if process:
                self.close()
                return request

    def close(self):
        self.s.close()
        self.s = None
    
    def processing_html(self):
        return """
        
        <!DOCTYPE html>
        <html>
        <head>
        	<!--To prevent favicon.ico requests-->
        	<link rel="icon" href="data:;base64,iVBORw0KGgo="> 
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        </head>
        <body>

        <h2>Processing data</h2>

        <p>Please wait... a few seconds</p>
        <p>If successful, the server will close, otherwise, hit refresh</p>
        <form>
            <a href="/"><button>Refresh</button></a>
        </form>

        </body>
        </html>"""

    def get_html(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
        	<!--To prevent favicon.ico requests-->
            <meta charset="utf-8">
        	<link rel="icon" href="data:;base64,iVBORw0KGgo=">
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        </head>
        <body>

        <h2>The select Element</h2>

        <p>The select element defines a drop-down list:</p>

        <form action="/" method="post" enctype="text/plain">
          <label for="ssid">Choose a car:</label>
          <select id="ssid" name="ssid">
            <option value="volvo">Volvo</option>
            <option value="saab">Saab</option>
            <option value="fiat">Fiat</option>
            <option value="audi">Audi</option>
          </select>
          <br><br>
          <label for="psswd">Password:</label>
          <input type="text" id="psswd" name="psswd" value=""><br><br>
          <input type="submit">
        </form>

        </body>
        </html>
    
        """

""" simple http server to serve up a config.json file
    Usage:
        python main.py

        This will start a server on port 8000
        You can then access the config.json file at http://localhost:8000/config.json
"""

import http.server
import socketserver
import ssl
import json
import os
from distutils.command.check import check
from logging import debug

ADDR = '192.168.11.30'
PORT = 8000

VERSION = '0.0.1'


class RemoteKill(Exception):
    pass

class Button_Not_Found(Exception):
    pass

def button_action(button_number):
    print (f"Button {button_number} pressed")


class ConfigHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

        if self.path == '/config.json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with open('config.json', 'r') as f:
                responce = f.read().encode()
                print(responce)
            self.wfile.write(responce)

        elif self.path == '/kill':
            raise RemoteKill()

        # If the path is one of the Button Actions defined in the config.json file
        # call button_action(button_name)
        elif self.path.startswith('/button/'):
            button_number = self.path.split('/')[-1]
            try:
                button_action(button_number)
            except Button_Not_Found:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Button Not Found')


        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def main():
    # print a start up message with the version number and url
    print(f"Starting simple server version {VERSION}")
    print(f"Serving config.json at http://{ADDR}:{PORT}/config.json")


    with socketserver.TCPServer((ADDR, PORT), ConfigHandler) as httpd:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        print("serving at port", PORT)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        except RemoteKill:
            pass
        finally:
            httpd.server_close()
            # check that the port is released
            if os.system(f"lsof -i :{PORT} | grep LISTEN | awk '{{print $2}}' | xargs kill -9") == 0:
                print("Port released")
            print("Server stopped and port released")

if __name__ == "__main__":
    main()


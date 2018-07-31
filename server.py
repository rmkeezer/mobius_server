#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import requests
import random
import cgi

hostName = "0.0.0.0"
hostPort = 5000

class MyServer(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200, "ok")
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.end_headers()

    #	GET is for clients geting the predi
    def do_GET(self):
        self.send_response(200)
        print("TEST")
        self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))

    #	POST is for submitting data.
    def do_POST(self):
        self._set_headers()

        print( "incomming http: ", self.path )

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'})

        print(form.getvalue("url"))
        self.wfile.write(json.dumps({"a":"test"}).encode('utf-8'))
        return

        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass


myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
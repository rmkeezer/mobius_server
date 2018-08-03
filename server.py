#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

import os
os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import requests
import random
import cgi

from scoreSong import init, scoreMp3
model = init()

import youtube_dl
postprocessors = []
postprocessors.append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': None,
            'nopostoverwrites': None,
})
ydl_opts = {
    'postprocessors': postprocessors,
    'outtmpl': 'songs/%(title)s-%(id)s.%(ext)s'
}
ydl = youtube_dl.YoutubeDL(ydl_opts)

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
        #self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))

    #	POST is for submitting data.
    def do_POST(self):
        self._set_headers()

        print( "incomming http: ", self.path )

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'})

        url = form.getvalue("url")
        print(url)
        
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict['title'].replace('"',"'").replace(":"," -")
        mp3fn = title + '-' + info_dict['id']

        if not os.path.exists('songs/' + mp3fn + '.mp3'):
            ydl.download([url])

        scoreMp3(mp3fn, model)

        self.wfile.write(json.dumps({"filename":mp3fn}).encode('utf-8'))
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
from libs import *
import socket
from threading import Thread
import codecs
from socketserver import StreamRequestHandler


class WebSocketHandler(StreamRequestHandler):
    def __init__(self,  socket, addr, server):
        Thread.__init__(self)
        self.server = server
        StreamRequestHandler.__init__(self, socket, addr, server)
    
    def connect(self):
        request = self.server.recv(10000).decode('utf-8')
        print(request)
        response = req_handshake(request)
        self.server.sendall(response.encode('ascii'))

        while (True):
            buff = self.server.recv(10000)
            print("wait for print")
            # keluarnya aneh
            print(buff)
from libs import *
import socket
from threading import Thread
import codecs
from socketserver import StreamRequestHandler
from framing import *

class WebSocketHandler(StreamRequestHandler):
    def __init__(self,  socket, addr, server):
        Thread.__init__(self)
        self.server = server
        StreamRequestHandler.__init__(self, socket, addr, server)
    
    def connect(self):
        request = self.server.recv(10000).decode('utf-8')
        print(request)
        
        # disini parse frame
        # kalo hasil parsenya berupa header handshake,
        response = req_handshake(request)
        self.server.sendall(response.encode('ascii'))
        # else
        while (True):
            buff = self.server.recv(10000)
            payload = parse(buff)
            print(payload['PAYLOAD'].decode())
        # !echo, !submission, ping pong
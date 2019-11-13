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
        self.server.send(response.encode('ascii'))
        # else
        while (True):
            buff = self.server.recv(10000)
            payload = parse(buff)

            mss = payload['PAYLOAD'].decode()
            received_message = mss.split(' ', 1)
            if received_message[0] == '!echo':
                if len(received_message) > 1:
                    packet = build(payload, "echo")
                    self.server.send(packet)
                else:
                    packet = build(payload, "")
                    self.server.send(packet)
            else:
                packet = build(payload, "")
                self.server.send(packet)


        # !echo, !submission, ping pong
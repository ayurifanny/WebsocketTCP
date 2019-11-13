from libs import *
import socket
from threading import Thread
import codecs
from socketserver import StreamRequestHandler
from framing import *
import threading

class WebSocketHandler(StreamRequestHandler):
    def __init__(self,  socket, addr, server):
        self.server = server
        StreamRequestHandler.__init__(self, socket, addr, server)
        server_thread = threading.Thread(target=self.connect)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()


    def connect(self):
        request = self.server.recv(10000).decode('utf-8')
        # print(request)
        # disini parse frame
        # kalo hasil parsenya berupa header handshake,
        response, self.handshake_done = req_handshake(request)
        print(self.handshake_done)
        self.server.send(response.encode('ascii'))
        # else
        while (self.handshake_done):
            buff = self.server.recv(10000)
            payload = parse(buff)

            opcode = payload['OPCODE']
            print(opcode)

            if opcode == 1:
                mss = payload['PAYLOAD'].decode()
                received_message = mss.split(' ', 1)
                if received_message[0] == '!echo':
                    if len(received_message) > 1:
                        packet = build(payload, "echo")
                        self.server.send(packet)
                    else:
                        packet = build(payload, "")
                        self.server.send(packet)
                elif received_message[0] == "!submission":
                    packet = buildFile("hello.docx")
                    self.server.send(packet)
            elif opcode == 2:
                sendBin(payload, "hello.docx")
            elif opcode == 8:
                still_alive = False
                return
            elif opcode == 9:
                mss = payload['PAYLOAD'].decode()
                received_message = mss.split(' ', 1)
                if received_message[0] == '!echo':
                    if len(received_message) > 1:
                        packet = build(payload, "echo")
                        self.server.send(packet)
                    else:
                        packet = build(payload, "")
                        self.server.send(packet)
                elif received_message[0] == "!submission":
                    packet = buildFile("hello.docx")
                    self.server.send(packet)
            elif opcode == 10:
                pass

        # !echo, !submission, ping pong


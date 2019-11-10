import socket
from libs import *
from WebSocketHandler import *
from socketserver import ThreadingMixIn, TCPServer

class WebSocket(ThreadingMixIn, TCPServer):
	def __init__(self, host, port):
		self.host = host
		self.port = port
		TCPServer.__init__(self, (host, port), WebSocketHandler)

	def connect_websocket(self):
		while (True):
			conn, addr = self.socket.accept()
			print("accepted connection from {}".format(addr))
			ws_connect = WebSocketHandler(self.socket,addr,conn)
			ws_connect.connect()

host = "127.0.0.1"
port = 9001
serv = WebSocket(host, port)
serv.connect_websocket()
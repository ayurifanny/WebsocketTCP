import socket
from libs import *
from WebSocketHandler import *
from socketserver import ThreadingMixIn, TCPServer
import threading


class WebSocket(ThreadingMixIn, TCPServer):
	allow_reuse_address = True  # TCP Server class's attribute
	daemon_threads = True  # comment to keep threads alive until finished
	clients = []
	id_counter = 0

	def __init__(self, host, port):
		self.host = host
		self.port = port
		TCPServer.__init__(self, (host, port), WebSocketHandler)

	def connect_websocket(self):
		while (True):
			conn, addr = self.socket.accept()
			print("accepted connection from {}".format(addr))
			ws_connect = WebSocketHandler(self.socket,addr,conn)
			self._new_client_(ws_connect)
	
	def _new_client_(self, handler):
		self.id_counter += 1
		client = {
			'id': self.id_counter,
			'handler': handler,
			'address': handler.client_address
		}
		print("called")
		self.clients.append(client)
		
	def handler_to_client(self, handler):
		for client in self.clients:
			if client['handler'] == handler:
				return client

host = "127.0.0.1"
port = 9001
serv = WebSocket(host, port)
serv.connect_websocket()

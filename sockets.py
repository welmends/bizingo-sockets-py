from socket import *

def get_localhost_ip():
	s = socket(AF_INET, SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip = s.getsockname()[0]
	s.close()
	return ip

class SocketP2P:
	def __init__(self, ip, port):
		self._sock_srv = socket(AF_INET, SOCK_STREAM)
		self._sock_srv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self._sock_clt = socket(AF_INET, SOCK_STREAM)
		self._sock_clt.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self._ip   = ip
		self._port = port
		if ip == 'localhost':
			self._ip = get_localhost_ip()

	def connect(self):
		#Client Mode
		self._peer = 'client'
		try:
			self._sock_clt.connect((self._ip, self._port))
			print('### Client Connected ###')
		except:
			# Server Mode
			self._peer = 'server'
			try:
				self._sock_srv.bind((self._ip, self._port))
				self._sock_srv.listen(1)
				(self._sock_clt, address) = self._sock_srv.accept()
				print('### Server Connected ###')
			except:
				# Failed
				self._peer = 'none'
				print('### Connection Failed ###')
				
	def peer_type(self):
		return self._peer

	def close(self):
		self._sock_srv.close()

	def receive(self):
		return self._sock_clt.recv(2048).decode("utf-8")

	def send(self, packet):
		self._sock_clt.send(packet.encode("utf-8"))
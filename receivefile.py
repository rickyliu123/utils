import socket,ssl
import hashlib

class otaDownloader:

	def __init__(self,server,port,ca,cert,key):
		self.ssl = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
		self.ssl.load_verify_locations(ca)
		self.ssl.check_hostname = False
		self.ssl.load_cert_chain(cert,key)			
		self.server = server
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ssock = self.ssl.wrap_socket(self.sock)
					
	def receive(self):
		try:
			self.ssock.connect((self.server,self.port))
		except ssl.SSLError:
			print(r'Failed to create socket ,exception ')	
		l = self.ssock.recv(1024)
		with open(r'test.bin',r'wb') as f:
			while (l):
				f.write(l)
				l = self.ssock.recv(1024)				
				#print(l)			
if __name__ == "__main__":
	dl = otaDownloader(r'65.49.198.6',11221,r'rootCA.crt',r'mqttclient.crt',r'mqttclient.key')
	dl.receive()


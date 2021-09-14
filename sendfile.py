import socket,ssl
import hashlib
import time


class fileSender:

	def __init__(self,ca,cert,key):
		self.sslCtx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
		self.sslCtx.load_cert_chain(cert,key)
		self.sslCtx.load_verify_locations(ca)
		self.sslCtx.verify_mode = ssl.CERT_REQUIRED
		#self.sslCtx.check_hostname = False
		
	# def __enter__(self):
		# return self
		
	# def __exit__(self, exc_type, exc_value, traceback):
		# pass
		
	def send(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.bind((r'0.0.0.0',11221))			
			sock.listen(5)
			while True:	
				try:
					ssock = self.sslCtx.wrap_socket( sock.accept()[0],server_side = True )
					with open(r'test.bin',r'rb') as f:
						l = f.read(1024)
						while (l):
							ssock.send(l)
							l = f.read(1024)
					ssock.shutdown(socket.SHUT_RDWR)
					ssock.close()					
				except:
					pass

		
	



if __name__ == "__main__":
	sender = fileSender(r'rootCA.crt',r'mqttserver.crt',r'mqttserver.key')
	sender.send()


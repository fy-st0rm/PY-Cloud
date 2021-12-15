import socket
import sys


# Protocols codes
protocols = {
	"login"	: "0",
	"singup": "1",
	"push"	: "2",
	"pull"	: "3",
	"share"	: "4"
}	
	

class PYC:
	def __init__(self, argv):
		# Server info
		self.ip = "127.0.0.1"
		self.port = 5050

		self.argv = argv

	def __connect(self):
		try:
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.client.connect((self.ip, self.port))
		except:
			print("Failed to connect to server! Check your internect connection or try later.")

	def run(self):
		self.__connect()
		
		self.argv[1] = self.argv[1].lower()
		if self.argv[1] not in protocols:
			print("Unknown protocls!")
			exit()
		
		# Protocol handling
		protocol_code = protocols[self.argv[1]]
		if protocol_code == "0":
			self.client.send(protocol_code.encode())
		elif protocol_code == "1":
			self.client.send(protocol_code.encode())
		elif protocol_code == "2":
			self.client.send(protocol_code.encode())
		elif protocol_code == "3":
			self.client.send(protocol_code.encode())
		elif protocol_code == "4":
			self.client.send(protocol_code.encode())

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print("Usage: pyc [protocol]")
		exit()

	pyc = PYC(sys.argv)
	pyc.run()


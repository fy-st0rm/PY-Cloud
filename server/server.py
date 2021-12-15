import socket
import time
import threading


# Protocols needed to be implemented:
# 1. login
# 2. signup
# 3. push
# 4. pull
# 5. share?	(To share files with other user)


# Protocols codes
LOGIN	= 0
SINGUP	= 1
PUSH	= 2
PULL	= 3
SHARE	= 4


class Server:
	def __init__(self):
		self.ip = "127.0.0.1"
		self.port = 5050
		self.buffer = 1024

		self.running = True

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind((self.ip, self.port))

	def __handle_client(self, conn):
		# Handle server protocols
		protocol = int(conn.recv(self.buffer).decode())
		
		if protocol == LOGIN:
			print("Do login!")
		elif protocol == SINGUP:
			print("Do singup!")
		elif protocol == PUSH:
			print("Do push!")
		elif protocol == PULL:
			print("Do pull!")
		elif protocol == SHARE:
			print("Do share!")

		conn.close()

	def run(self):
		self.server.listen()
		print(f"Server listening in {self.ip}")
		
		while self.running:
			conn, addr = self.server.accept()
			
			new_thread = threading.Thread(target=self.__handle_client, args=(conn, ))
			new_thread.start()


if __name__ == "__main__":
	server = Server()
	server.run()

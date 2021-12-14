import socket
import time
import threading


# Protocols needed to be implemented:
# 1. login
# 2. signup
# 3. push
# 4. pull
# 5. share?	(To share files with other user)


class Server:
	def __init__(self):
		self.ip = "127.0.0.1"
		self.port = 5050

		self.running = True

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind((self.ip, self.port))

	def __handle_client(self, conn):
		# Handle server protocols
		print(conn)


	def run(self):
		self.server.listen()
		print(f"Server listening in {self.ip}")
		
		while self.running:
			conn, addr = self.server.accept()
			
			new_thread = threading.Thread(target=self.__handle_client, args=(conn, ))
			new_thread.start()



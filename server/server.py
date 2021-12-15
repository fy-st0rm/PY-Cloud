import socket
import time
import threading
import json
import os

# Protocols needed to be implemented:
# 1. login
# 2. signup
# 3. push
# 4. pull
# 5. share?	(To share files with other user)


# Protocols codes
LOGIN	= 0
SIGNUP	= 1
PUSH	= 2
PULL	= 3
SHARE	= 4


class Server:
	def __init__(self):
		self.ip = "127.0.0.5"
		self.port = 5050
		self.buffer = 1024

		self.running = True

		self.seperator = "[se]"

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind((self.ip, self.port))

		

	def __handle_client(self, conn):
		# Handle server protocols
		protocol = int(conn.recv(self.buffer).decode())
		
		if protocol == LOGIN:
			print("Do login!")
		elif protocol == SIGNUP:

			#re-receives the signup data
			self.__userData = conn.recv(self.buffer).decode()
			self.__userData = self.__userData.split(self.seperator)

			self.__username = self.__userData[0]
			self.__password = self.__userData[1]

			#Checks and writes data in user data json file
			with open("userdata/userdata.json", "r") as dataFile: 
				self.__file = json.load(dataFile)

			if self.__username in self.__file:
				conn.send("-5".encode())
			else:
				self.__userDetail = {"password":self.__password}
				self.__file.update({self.__username:self.__userDetail})
				with open("userdata/userdata.json", "w") as dataFile:
					json.dump(self.__file, dataFile)

				os.mkdir(f"userfiles/{self.__username}")
				conn.send("5".encode())



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

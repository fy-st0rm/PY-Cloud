import socket
import json
import os
import sys
import getpass
import time


# Protocols codes
ERROR = -1
SUCESS=  1
protocols = {
	"login"	: "100",
	"signup": "101",
	"push"	: "200",
	"pull"	: "201",
	"share"	: "202"
}	
	

class PYC:
	def __init__(self, argv):
		# Server info
		self.ip = "127.0.0.5"
		self.port = 5050
		self.buffer = 61440
		self.packet_size = 46080

		self.argv = argv
		self.seperator = "<sep>"

	def __connect(self):
		try:
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.client.connect((self.ip, self.port))
		except:
			print("Failed to connect to server! Check your internect connection or try later.")

	def __send(self, data):
		time.sleep(0.1)
		self.client.send(data.encode())

	#------------------Account handling section--------------------#

	#For checking Usr Name
	def __check_username(self, username):
		length = len(username)
		if length <= 3:
			print("Error: Minimum number of character of a username is 3")
			exit()
		elif length >= 15:
			print("Error: Maximum number of chacter of a username is 15")
			exit()

	#For checking Usr Pswd
	def __check_password(self, password):
		if len(password) <= 3:
			print("Error: Minimum number of character of a password is 3")
			exit()
	
	def __signup(self, protocol_code):
		#Asking for user data
		self.username = input("Username: ")
		self.password = getpass.getpass()

		#Checking username and passwrd
		self.__check_username(self.username)
		self.__check_password(self.password)

		#User Data
		self.__user_data = f"{self.username}{self.seperator}{self.password}"

		#Sends Protocol Code
		self.client.send(protocol_code.encode())

		#Waits For Protocol Code to reach
		time.sleep(0.1)

		#Sends the userdata
		self.client.send(self.__user_data.encode())

		#Receives Responce
		self.__resp = int(self.client.recv(self.buffer).decode())

		#Shows status of the account creation
		if self.__resp == ERROR:
			#Faliure
			print("The account already exsists!")
			exit()
		elif self.__resp == SUCESS:
			#Creates file for auto sign up
			with open("usrdata","w") as self.__file:
				self.__file.write(f"{self.username}{self.seperator}{self.password}")
			#Sucess!
			print("The account has been registered!")
	
	def run(self):
		self.__connect()
		
		self.argv[1] = self.argv[1].lower()
		if self.argv[1] not in protocols:
			print("Unknown protocls!")
			self.client.send(str(ERROR).encode())
			exit()
		
		# Protocol handling
		protocol_code = protocols[self.argv[1]]
		if protocol_code == "100":
			self.client.send(protocol_code.encode())

		elif protocol_code == "101":
			self.__signup(protocol_code)

		elif protocol_code == "200":
			self.__send(protocol_code)
				
			file = self.argv[2]
			with open(file, "r") as r:
				file_data = r.read()
			
			padding = self.packet_size - (len(file_data) % self.packet_size)
			for padd in range(padding):
				file_data += "0"
			packet_size = int(len(file_data) / self.packet_size)

			file_info = f"{file}{self.seperator}{padding}{self.seperator}{packet_size}"
			self.__send(file_info)

			packets = {}
			packet_no = 0
			for i in range(0, len(file_data), self.packet_size):
				chunk = file_data[i:i+self.packet_size]
				packets[packet_no] = chunk
				#temp_packet = f"{packet_no}{self.seperator}{chunk}"
				print("Sending:", sys.getsizeof(chunk), "bytes..")
				packet_no += 1

				self.__send(chunk)

			self.__send(str(SUCESS))
			print("Total size:", sys.getsizeof(file_data), "bytes")
			print("Total packets:", len(packets), "bytes")

		elif protocol_code == "201":
			self.client.send(protocol_code.encode())
		elif protocol_code == "202":
			self.client.send(protocol_code.encode())

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print("Usage: pyc [protocol]")
		exit()

	pyc = PYC(sys.argv)
	pyc.run()


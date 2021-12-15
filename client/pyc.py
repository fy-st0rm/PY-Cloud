import socket
import sys
import getpass
import time


# Protocols codes
protocols = {
	"login"	: "0",
	"signup": "1",
	"push"	: "2",
	"pull"	: "3",
	"share"	: "4"
}	
	

class PYC:
	def __init__(self, argv):
		# Server info
		self.ip = "127.0.0.5"
		self.port = 5050
		self.buffer = 1024

		self.argv = argv
		self.seperator = "[se]"

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

			#Asking for user data
			self.username = input("Username: ")
			self.password = getpass.getpass()

			#Checking username and passwrd
			self.checkUsername(self.username)
			self.checkPassword(self.password)

			#User Data
			self.__userData = f"{self.username}{self.seperator}{self.password}"

			#Sends Protocol Code
			self.client.send(protocol_code.encode())

			#Waits For Protocol Code to reach
			time.sleep(0.1)

			#Sends the userdata
			self.client.send(self.__userData.encode())

			#Receives Responce
			self.__resp = int(self.client.recv(self.buffer).decode())

			#Shows status of the account creation
			if self.__resp == -5:
				#Faliure
				print("The account already exsists!")
				exit()
			elif self.__resp == 5:
				#Creates file for auto sign up
				with open("usrdata","w") as self.__file:
					self.__file.write(f"{self.username}{self.seperator}{self.password}")
				#Sucess!
				print("The account has been registered!")

		elif protocol_code == "2":
			self.client.send(protocol_code.encode())
		elif protocol_code == "3":
			self.client.send(protocol_code.encode())
		elif protocol_code == "4":
			self.client.send(protocol_code.encode())

	#For checking Usr Name
	def checkUsername(self,__username):
		self.__username = __username
		self.__usernamelen = len(self.__username)
		if self.__usernamelen <= 3:
			print("Error: Minimum number of character of a username is 3")
			exit()
		elif self.__usernamelen >= 15:
			print("Error: Maximum number of chacter of a username is 15")
			exit()
		else:
			pass

	#For checking Usr Pswd
	def checkPassword(self,__password):
		self.__password = __password
		self.__passwordlen = len(self.__password)
		if self.__passwordlen <= 3:
			print("Error: Minimum number of character of a password is 3")
			exit()
		else:
			pass

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print("Usage: pyc [protocol]")
		exit()

	pyc = PYC(sys.argv)
	pyc.run()


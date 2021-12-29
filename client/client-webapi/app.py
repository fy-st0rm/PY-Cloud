import eel
from pyc import*


@eel.expose
def _login(username, password):
	pyc = PYC()
	print("Sending login info....")
	result = int(pyc.login("100", username,password))
	if result == -1:
		eel.alert_login("Your account doesnt exsists! Try Signing up!")
	if result == 1:
		eel.alert_login("Account Logged in sucessfully!")

@eel.expose
def _signup(username, password):
	pyc = PYC()
	print("Sending signup info....")
	result = int(pyc.login("101", username, password))
	if result == -1:
		eel.alert_login("Your account already exsists!")
	if result == 1:
		eel.alert_login("your account is create sucessfully!")


eel.init("ui")
eel.start("login.html",  mode = "default")





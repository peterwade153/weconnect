""" 
classs for weconnect
"""
import sys
sys.path.append('..')
from users import User
from business import Business
from review import Review 


class weconnect():
	"""docstring fos weconnect"""

	def __init__(self):

		self.users = {}
		self.businesses = {}

	def register_user(self, username, password):
		""" method for registering a user"""

		if users.get(username):
			return "User registered already"

		new_user = User(username, password)
		self.users[username] = new_user

	def register_business(self, current_user, business_name):
		new_business = Business(current_user, business_name)
		self.businesses[business_name] = new_business

	def login(self, username, password):
		""" method for logging in """
		
		if {username: password} in self.users:
			return 1
		else:
			return 0

	def reset_password(self, username, password, new_password):
		""" method for reseting a user password """

		if {username: password} in self.users:
			self.user[username] = new_password
			return self.user
		else:
			return "user not registered here"


def main():

	myuser = weconnect()
	myuser.register_user(james, test123)
	myuser.login(james,test123)
	myuser.reset_password(james, test123, test12345)

	print(myuser.users)
	print(myuser.register_user(james, test123))
	print(myuser.login(james,test123))
	print(myuser.reset_password(james, test123, test12345)

if __name__ == '__main__':
	main()
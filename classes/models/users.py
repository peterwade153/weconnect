"""
class for users
"""

class User():
	"""docstring for User"""

	def __init__(self, username, password):

		self.username = username
		self.password = password
		self.businesses = []

	def add_user(self, username, password):
		""" method for adding a user"""

		self.user = {}
		self.user[username] = password
		return self.user


	def register_business(self, business_name):
		""" method for registering a business """

		my_business = business.add_business(business_name)
		return self.businesses.append(my_business)

	def view_businesses(self):
		""" methods for viewing businesses """

		return self.businesses

	def view_a_business(self, id):
		""" method to view a business """

		for business in businesses:
			if business.has_key(id):
				return business

			else:
				return "business not registered"


	def update_a_business(self, id, new_name):
		""" method for updating abusiness """

		for business in businesses:
			if business.has_key(id):
				business[id] = new_name
				return business
			else:
				return "business not registered"


	def delete_business(self, id):
		"""method for deleting a business """

		if self.businesses.get(id):
			del self.businesses[id]



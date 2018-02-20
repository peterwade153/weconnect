class User(object):
	"""docstring for user"""
	def __init__(self):
		self.business = {}
		self.business_reviews = {}

	def register_business(self, id, business_name):
		""" method allows a user to register a business"""

		#checking if user is not registered already
		if id not in self.business.keys() and business_name not in self.business.values():
			self.business[id] = business_name
		else:
			return "business already registered"
		return self.business

	def view_registered_businesses(self):
		""" method allows a user to view all registered businesses"""

		my_list = []

		for business in self.business.values():
			my_list.append(business)

		return my_list

	def view_a_business(self, id):
		""" method allows a user to a view a business"""
		if id in self.business.keys():
			my_business = self.business[id]

		else:
			"business not registered!"

		return my_business


		  
	def update_registered_business(self, id, new_name):
		""" method allows a user update a registered business"""

		if id in self.business.keys():
			self.business[id] = new_name

		else:
			return "business doesnot exist!"

		return self.business

	def delete_registered_business(self, id):
		""" method allows a user delete a business they registered"""

		if id in self.business.keys():
			del self.business[id]
		else:
			return "business doesnot exist"

		return self.business

	def add_review(self, id, review):
		""" method allows a user add a review to a registered business"""

		if id in self.business.keys():
			if id in self.business_reviews.keys():
				(self.business_reviews[id]).append(review)

			else:
				reviews = []
				reviews.append(review)
				self.business_reviews[id] = reviews

		else:
			return "business doesnt exist!"

		return self.business_reviews

	def view_business_reviews(self, id):
		""" shows reviews of a business"""

		my_list = []
		if id in self.business.keys():
			if id in self.business_reviews.keys():
				for review in self.business_reviews[id]:
					my_list.append(review)


			else:
				return "business currently has no reviews"

		else:
			return "business doest exist!"

		return my_list



	def view_reviews(self):
		""" method allows a user to view business reviews"""

		my_list = []
		for review in self.business_reviews.values():
			my_list.append(review)
		return my_list





def main():
	biz = User()
	biz.register_business(1,'roko')
	biz.register_business(2,'rocks')
	biz.register_business(3,'fruits')
	biz.update_registered_business(2,'ugs')
	biz.delete_registered_business(2)
	biz.add_review(3,'lovely')
	biz.add_review(3,'smart')
	biz.add_review(1,'quick')

	biz.view_a_business(1)

	print(biz.business)
	print(biz.view_registered_businesses())
	print(biz.view_reviews())
	print(biz.view_business_reviews(3))

if __name__ == '__main__':
	main() 






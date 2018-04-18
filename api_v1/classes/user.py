""" user class"""

class User():
	"""docstring for user"""
	def __init__(self):
		
		self.businesses = {}
		self.business_reviews = {}

	def register_business(self, business_name):
		""" method allows a user to register a business"""

		if business_name not in self.businesses.values():
			if len(self.businesses.keys()) == 0:
				id = 1
			else:
				id = (max(self.businesses.keys())) + 1

			self.businesses[id] = business_name
			business = {"id": id, "business_name": business_name}
			return business
		return False


	def view_registered_businesses(self):
		""" method allows a user to view all registered businesses"""

		return self.businesses

	def view_a_business(self, id):
		""" method allows a user to a view a business"""

		return self.businesses.get(id, "business not registered")

		  
	def update_registered_business(self, id, new_name):
		""" method allows a user update a registered business"""

		if id in self.businesses.keys():
			self.businesses[id] = new_name.strip()
		
		return self.businesses.get(id, "business not registered")




	def delete_registered_business(self, id):
		""" method allows a user delete a business they registered"""

		if id in self.businesses.keys():
			business_name = self.businesses[id]
			del self.businesses[id]
			return "business {} deleted successfully".format(business_name)
		else:
			return "business doesnot exist"



	def add_review(self, id, review):
		""" method allows a user add a review to a registered business"""

		if self.businesses.get(id):
			if self.business_reviews.get(id):
				(self.business_reviews[id]).append(review)
			else:
				reviews = []
				review.strip()  #stripping any whitespaces user may pass in accidentally
				reviews.append(review)
				self.business_reviews[id] = reviews
		else:
			return "business doesnt exist!"

		return self.business_reviews

	def view_business_reviews(self, id):
		""" shows reviews of a business"""

		my_reviews = []
		if id in self.businesses.keys():
			if id in self.business_reviews.keys():
				for review in self.business_reviews[id]:
					my_reviews.append(review)

			else:
				return "business currently has no reviews"

		else:
			return "business doest exist!"

		return my_reviews


	def view_reviews(self):
		""" method allows a user to view business reviews"""

		all_reviews = []
		for review in self.business_reviews.values():
			all_reviews.append(review)
		return all_reviews





def main():
	biz = User()
	biz.register_business('roko')
	biz.register_business('rocks')
	biz.register_business('fruits')
	biz.update_registered_business(2,'ugs')
	biz.view_a_business(1)
	biz.delete_registered_business(2)
	biz.add_review(3,'lovely')
	biz.add_review(3,'smart')
	biz.add_review(1,'quick')

	biz.view_a_business(1)

	print(biz.businesses)
	print(biz.delete_registered_business(3))
	print(biz.view_registered_businesses())
	print(biz.view_a_business(3))
	print(biz.view_reviews())
	print(biz.view_business_reviews(3))

if __name__ == '__main__':
	main() 






""" user class"""

class User():
	"""docstring for user"""
	def __init__(self):
		self.id = 0
		self.businesses = {}
		self.business_reviews = {}

	def register_business(self, business_name):
		""" method allows a user to register a business"""

		self.id = (len(self.businesses.keys())) + 1
		#stripping any leading or tailing spaces
		business_name.strip()
		self.businesses[self.id] = business_name
		return self.businesses


	def view_registered_businesses(self):
		""" method allows a user to view all registered businesses"""

		return self.businesses

	def view_a_business(self, id):
		""" method allows a user to a view a business"""
		my_list = []
		if id in self.businesses.keys():
			my_business = self.businesses[id]
			my_list.append(my_business)

		else:
			return "business not registered!"

		return my_list

		  
	def update_registered_business(self, id, new_name):
		""" method allows a user update a registered business"""

		if id in self.businesses.keys():
			new_name.strip()  #stripping any leading or tailing spaces
			self.businesses[id] = new_name
		else:
			return "business doesnot exist!"
		return self.businesses

	def delete_registered_business(self, id):
		""" method allows a user delete a business they registered"""

		if id in self.businesses.keys():
			del self.businesses[id]
		else:
			return "business doesnot exist"

		return self.businesses

	def add_review(self, id, review):
		""" method allows a user add a review to a registered business"""

		if id in self.businesses.keys():
			if id in self.business_reviews.keys():
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






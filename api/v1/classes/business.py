"""business class"""

class Business():
	"""docstring for Business"""

	def __init__(self, user, business_name):
		""" constructor """

		self.business_name = business_name 
		self.reviews = []

	def add_business(self, business_name):
		""" addind a new business """

		self.business = {}
		self.business[id] = business_name
		return self.business

	def review_a_business( reviews):
		""" allows reviewing of a business """

		self.reviews.append(reviews)


	def view_reviews_for_business(business_id):
		""" viewing all business reviews """

		 return self.reviews


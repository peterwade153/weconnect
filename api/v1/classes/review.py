""" reviews class"""

class Review():
	"""doc string for Review"""
	def __init__(self, reviews):
		self.reviews = reviews
		
	def __repr__():
		return 'Reviews: ' + ','.join(review for review in self.reviews)

		
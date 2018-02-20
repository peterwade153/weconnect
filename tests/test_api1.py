import unittest

class BusinessTestCase(unittest.TestCase):

	def SetUp(self):
		""" this is run before every test"""
		pass

	def TearDown(self):
		""" this runs after every test"""
		pass

	def test_business_registered_successfully(self):
		""" tests a business can be created successfully """
		pass

	def test_registering_already_existing_business(self):
		""" tests a business cant be registered more than once"""
		pass

	def test_editing_registered_business(self):
		""" tests a business can be updated """
		pass


	def test_deleting_registered_business(self):
		""" tests a business can be deleted"""
		pass

	def test_adding_review(self):
		""" tests adding a review to a business """
		pass

	def test_viewing_registered_business():
		""" tests viewing business reviews """
		pass

if __name__ == '__main__':
	unittest.main()
import json
import unittest
from app import app

class BusinessTestCase(unittest.TestCase):

	def SetUp(self):
		""" this is run before every test"""
		self.app = app.test_client()
		app.testing = True

	def TearDown(self):
		""" this runs after every test"""
		pass

	def test_user_registration(self):
		""" tests user is registered """

		user_data = {'username': 'test', 'password':'test123'}
		result = self.app.post('/api/v1/auth/register', data = json.dumps(user_data))
		self.assertIn('registered successfully', str(result.data))
		self.assertEqual(result.status_code, 201)


	def test_user_login(self):
		""" tests a user can login """

		user_data = {'username': 'test', 'password':'test123'}
		result2 = self.app.post('/api/v1/auth/login', data = json.dumps(user_data))
		self.assertIn('logged in successfully!', str(result2.data))
		self.assertEqual(result2.status_code, 200)



	def test_business_registered_successfully(self):
		""" tests a business can be created successfully """

		business_data = {'id': 1, 'business_name':'demo'}


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
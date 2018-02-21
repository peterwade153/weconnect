import sys
sys.path.append('..')
import json
import unittest
from app.app import app

class BusinessTestCase(unittest.TestCase):

	def setUp(self):
		""" this is run before every test"""

		self.app = app.test_client()
		self.app.testing = True
		

	def tearDown(self):
		""" this runs after every test"""
		pass

	def test_user_registration(self):
		""" tests user is registered """

		user_data = {'username': 'test', 'password': 'test123'}
		result = self.app.post('/api/v1/auth/register', data = json.dumps(user_data), content_type= 'application/json')
		self.assertIn('registered successfully', str(result.data))
		self.assertEqual(result.status_code, 201)


	def test_user_login(self):
		""" tests a user can login """

		user_data = {'username': 'test', 'password': 'test123'}
		result = self.app.post('/api/v1/auth/register', data = json.dumps(user_data), content_type= 'application/json')
		result2 = self.app.post('/api/v1/auth/login', data = json.dumps(user_data), content_type= 'application/json')
		self.assertIn('logged in successfully!', str(result2.data))
		self.assertEqual(result2.status_code, 200)



	def test_business_registered_successfully(self):
		""" tests a business can be created successfully """

		business_data = {'id': 1, 'business_name': 'demo'}
		res = self.app.post('/api/v1/businesses', data = json.dumps(business_data))
		self.assertIn('demo', str(res.data))
		self.assertEqual(res.status_code, 201)


	def test_registering_already_existing_business(self):
		""" tests a business cant be registered more than once"""

		business_data = {'id': 1, 'business_name': 'demo'}
		rev = self.app.post('/api/v1/businesses', data = json.dumps(business_data))
		self.assertEqual(rev.status_code, 201)
		res = self.post('/api/v1/businesses', data = json.dumps(business_data))
		self.assertIn('Business registered already', str(res.data))


	def test_editing_registered_business(self):
		""" tests a business can be updated """
		
		business_data = {'id': 1, 'business_name': 'demo'}
		rev = self.app.post('/api/v1/businesses', data = json.dumps(business_data))
		self.assertEqual(rev.status_code, 201)
		new_data = {'id': 1, 'new_name': 'roko'}
		update_res = self.put('/api/v1/businesses/1', data = json.dumps(new_name))
		self.assertIn('roko', str(update_res.data))
		self.assertEqual(update_res.status_code, 200)


	def test_deleting_registered_business(self):
		""" tests a business can be deleted"""

		business_data = {'id': 1, 'business_name': 'demo'}
		rev = self.app.post('/api/v1/businesses', data = json.dumps(business_data))
		self.assertEqual(rev.status_code, 201)
		del_result = self.app.delete('/api/v1/businesses/1')
		self.assertEqual(del_result.status_code, 200)


	def test_adding_review(self):
		""" tests adding a review to a business """

		business_data = {'id': 1, 'business_name': 'demo'}
		rev = self.app.post('/api/v1/businesses', data = json.dumps(business_data))
		self.assertEqual(rev.status_code, 201)
		review = {'id': 'Fantastic'}
		review_res = self.app.post('/api/v1/1/reviews', data = json.dumps(review))
		self.assertEqual(review_res.status_code, 201)


	def test_viewing_registered_business(self):
		""" tests viewing business reviews """

		business_data = {'id': 1, 'business_name': 'demo'}
		rev = self.app.post('/api/v1/businesses', data = json.dumps(business_data))
		self.assertEqual(rev.status_code, 201)
		review = {'id': 'Fantastic'}
		review_res = self.app.post('/api/v1/businesses/1/reviews', data = json.dumps(review))
		self.assertEqual(review_res.status_code, 201)
		get_res = self.app.get('/api/v1/businesses/1/reviews')
		self.assertEqual(get_res.status_code, 200)




if __name__ == '__main__':
	unittest.main()

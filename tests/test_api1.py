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

		user_data = {'username': 'test1', 'password': 'test1273'}
		result = self.app.post('/api/v1/auth/register', data = json.dumps(user_data), content_type = 'application/json')
		self.assertEqual(result.status_code, 201)
		self.assertIn('registered successfully', str(result.data))
		

	def test_user_only_registers_with_requires_data(self):
		""" tests a user has to provide all required fields"""

		user_data = {'username': '', 'password': ''}
		result = self.app.post('/api/v1/auth/register', data = json.dumps(user_data), content_type = 'application/json')
		self.assertEqual(result.status_code, 400)



	def test_user_only_registers_once(self):
		""" test user cant register twice"""

		user_data = {'username': 'test', 'password': 'test1023'}
		result = self.app.post('/api/v1/auth/register', data = json.dumps(user_data), content_type = 'application/json')
		self.assertIn('registered successfully', str(result.data))
		res = self.app.post('/api/v1/auth/register', data = json.dumps(user_data), content_type = 'application/json')
		self.assertEqual(res.status_code, 202)


	def test_user_login(self):
		""" tests a user login """

		user_data = {'username': 'test2', 'password': 'test1236'}
		result = self.app.post('/api/v1/auth/register', data = json.dumps(user_data), content_type= 'application/json')
		self.assertEqual(result.status_code, 201)		
		result2 = self.app.post('/api/v1/auth/login', data = json.dumps(user_data), content_type= 'application/json')
		self.assertIn('logged in successfully!', str(result2.data))
		self.assertEqual(result2.status_code, 200)


	def test_non_registered_user_attempt_to_login(self):
		""" test a  non user registered user cant login """

		user_data = {'username': 'test32', 'password': 'test1234'}
		result2 = self.app.post('/api/v1/auth/login', data = json.dumps(user_data), content_type= 'application/json')
		self.assertEqual(result2.status_code, 401)



	def test_user_login_without_providing_data(self):
		""" test user cant login without providing credentials"""

		user_data = {'username': '', 'password': ''}
		result2 = self.app.post('/api/v1/auth/login', data = json.dumps(user_data), content_type= 'application/json')
		self.assertEqual(result2.status_code, 400)


	def test_user_can_reset_password(self):
		""" tests aregistered user can reset their password """

		user_data = {'username': 'test12', 'password': 'test12345'}
		result = self.app.post('/api/v1/auth/register', data = json.dumps(user_data), content_type = 'application/json')
		self.assertEqual(result.status_code, 201)
		new_data = {'username': 'test12', 'new_password': 'test123456'}
		res = self.app.post('/api/v1/auth/reset-password', data = json.dumps(new_data), content_type = 'application/json')
		self.assertEqual(res.status_code, 200)


	def test_only_registered_user_can_reset_password(self):
		""" only registered users should change passwords"""

		user_data = {'username': 'test112', 'password': 'test1233'}
		result = self.app.post('/api/v1/auth/register', data = json.dumps(user_data), content_type = 'application/json')
		self.assertEqual(result.status_code, 201)
		new_data = {'username': 'test12', 'new_password': 'test12345'}
		res = self.app.post('/api/v1/auth/reset-password', data = json.dumps(new_data), content_type = 'application/json')
		self.assertEqual(res.status_code, 404)



	def test_business_registered_successfully(self):
		""" tests a business can be created successfully """

		business_data = {'id': 1, 'business_name': 'demo'}
		res = self.app.post('/api/v1/businesses', data = json.dumps(business_data), content_type= 'application/json')
		self.assertIn('Business registered successfully', str(res.data))
		self.assertEqual(res.status_code, 201)


	def test_editing_registered_business(self):
		""" tests a business can be updated """
		
		business_data = {'id': 1, 'business_name': 'demo'}
		rev = self.app.post('/api/v1/businesses', data = json.dumps(business_data), content_type = 'application/json')
		self.assertEqual(rev.status_code, 201)
		new_data = {'id': 1, 'new_name': 'roko'}
		update_res = self.app.put('/api/v1/businesses/1', data = json.dumps(new_data), content_type = 'application/json')
		self.assertIn('Business updated successfully!', str(update_res.data))
		self.assertEqual(update_res.status_code, 200)


	def test_deleting_registered_business(self):
		""" tests a business can be deleted"""

		business_data = {'id': 1, 'business_name': 'demo'}
		rev = self.app.post('/api/v1/businesses', data = json.dumps(business_data), content_type = 'application/json')
		self.assertEqual(rev.status_code, 201)
		del_result = self.app.delete('/api/v1/businesses/1', content_type= 'application/json')
		self.assertEqual(del_result.status_code, 200)


	def test_adding_review(self):
		""" tests adding a review to a business """

		business_data = {'id': 1, 'business_name': 'demo'}
		rev = self.app.post('/api/v1/businesses', data = json.dumps(business_data), content_type = 'application/json')
		self.assertEqual(rev.status_code, 201)
		review = {'review': 'Fantastic'}
		review_res = self.app.post('/api/v1/businesses/1/reviews', data = json.dumps(review), content_type = 'application/json')
		self.assertEqual(review_res.status_code, 201)


	def test_viewing_registered_business(self):
		""" tests viewing business reviews """

		business_data = {'id': 1, 'business_name': 'demo'}
		rev = self.app.post('/api/v1/businesses', data = json.dumps(business_data), content_type = 'application/json')
		self.assertEqual(rev.status_code, 201)
		review = {'review': 'Fantastic'}
		review_res = self.app.post('/api/v1/businesses/1/reviews', data = json.dumps(review), content_type = 'application/json')
		self.assertEqual(review_res.status_code, 201)
		get_res = self.app.get('/api/v1/businesses/1/reviews')
		self.assertEqual(get_res.status_code, 200)




if __name__ == '__main__':
	unittest.main()

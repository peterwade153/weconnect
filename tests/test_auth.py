import sys
sys.path.append('..')
import json
import unittest
from app import app
from app.models import db


class AuthTestCase(unittest.TestCase):
	"""docstring for AuthTestCase"""

	def setUp(self):
		self.app = app.test_client()
		app.testing = True
		self.user_data = {'username':'demo',
		                  'email':'demo@test.com',
		                  'password':'demo12345'
		                  }

		with app.app_context():
			db.drop_all()
			db.create_all()


	def test_user_registration(self):
		""" tests user registration on the app """

		reg = self.app.post('/api/v2/auth/register', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(reg.status_code, 201)
		self.assertIn('Successfully registered', str(reg.data))


	def test_user_already_registered(self):
		""" tests a user cant register more than once """

		res = self.app.post('/api/v2/auth/register', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(res.status_code, 201)
		rev = self.app.post('/api/v2/auth/register', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(rev.status_code, 202)


	def tests_user_registering_with_invalid_data(self):
		""" tests invalid data in not allowed """

		users_data = {'username':'#$@#emo', 'email': 'testtest.com', 'password': '@##st1023'}
		reg = self.app.post('/api/v2/auth/register', data = json.dumps(users_data), content_type = 'application/json')
		self.assertEqual(reg.status_code, 403)


	def test_user_login(self):
		""" tests a user can login """

		reg = self.app.post('/api/v2/auth/register', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(reg.status_code, 201)
		rev = self.app.post('/api/v2/auth/login', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(rev.status_code, 200)


	def tests_non_registered_user_login(self):
		""" test non registered users cant be logged in """

		users_data = {'email': 'test@test.com', 'password': 'test1023'}
		reg = self.app.post('/api/v2/auth/login', data = json.dumps(users_data), content_type = 'application/json')
		self.assertEqual(reg.status_code, 401)  #unauthorized access


	def tests_wrong_password_user_login(self):
		""" test registered users cant be logged in with incorrect password """

		reg = self.app.post('/api/v2/auth/register', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(reg.status_code, 201)
		users_data = {'email':'demo@test.com', 'password': 'test1023'}
		reg = self.app.post('/api/v2/auth/login', data = json.dumps(users_data), content_type = 'application/json')
		self.assertEqual(reg.status_code, 401)  #unauthorized access


	def tests_user_logging_in_with_invalid_data(self):
		""" tests invalid data in not allowed """

		users_data = {'username':'#$@#emo', 'email': 'testtest.com', 'password': '@##st1023'}
		reg = self.app.post('/api/v2/auth/login', data = json.dumps(users_data), content_type = 'application/json')
		self.assertEqual(reg.status_code, 403)


	def tests_user_logout(self):
		""" test a user logs out successfully """

		reg = self.app.post('/api/v2/auth/register', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(reg.status_code, 201)
		rev = self.app.post('/api/v2/auth/login', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(rev.status_code, 200)
		token = json.loads(rev.data.decode())['token']
		result = self.app.post('/api/v2/auth/logout', headers = {'Content-Type':'application/json','Authorization':token})
		self.assertEqual(result.status_code, 200)

	def tests_already_logged_user_attempting_logout(self):
		""" tests double logout is not accepted """

		reg = self.app.post('/api/v2/auth/register', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(reg.status_code, 201)
		rev = self.app.post('/api/v2/auth/login', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(rev.status_code, 200)
		token = json.loads(rev.data.decode())['token']
		result = self.app.post('/api/v2/auth/logout', headers = {'Content-Type':'application/json','Authorization':token})
		self.assertEqual(result.status_code, 200)
		second = self.app.post('/api/v2/auth/logout', headers = {'Content-Type':'application/json','Authorization':token})
		self.assertEqual(second.status_code, 403)


	def test_user_reset_password(self):
		""" tests user successfully reset their passsword """

		reg = self.app.post('/api/v2/auth/register', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(reg.status_code, 201)
		rev = self.app.post('/api/v2/auth/login', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(rev.status_code, 200)
		token = json.loads(rev.data.decode())['token']

		new_data = {'email': 'demo@test.com', 'new_password': 'tests1233'}
		res = self.app.post('/api/v2/auth/reset-password', data = json.dumps(new_data), 
			                                  headers = {'Content-Type':'application/json','Authorization':token})
			                                                                                       
		self.assertEqual(res.status_code, 200)

	def test_user_reseting_password_for_another_user(self):
		""" tests you cant reset password for another user account """

		reg = self.app.post('/api/v2/auth/register', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(reg.status_code, 201)
		rev = self.app.post('/api/v2/auth/login', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(rev.status_code, 200)
		token = json.loads(rev.data.decode())['token']

		new_data = {'email': 'test@test.com', 'new_password': 'tests1233'}
		res = self.app.post('/api/v2/auth/reset-password', data = json.dumps(new_data), 
			                                  headers = {'Content-Type':'application/json','Authorization':token})
			                                                                                       
		self.assertEqual(res.status_code, 403)

	def tests_user_resetting_password_with_invalid_data(self):
		"""tests only valid charaters are allowed """

		reg = self.app.post('/api/v2/auth/register', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(reg.status_code, 201)
		rev = self.app.post('/api/v2/auth/login', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(rev.status_code, 200)
		token = json.loads(rev.data.decode())['token']

		new_data = {'email': '#$%test@test.com', 'new_password': '$%%tests1233'}
		res = self.app.post('/api/v2/auth/reset-password', data = json.dumps(new_data), 
			                                  headers = {'Content-Type':'application/json','Authorization':token})
			                                                                                       
		self.assertEqual(res.status_code, 403)

	def test_non_user_attempting_password_reset(self):
		""" tests only registered users can rest passwords """

		new_data = {'email': 'test@test.com', 'new_password': 'tests1233'}
		res = self.app.post('/api/v2/auth/reset-password', data = json.dumps(new_data), 
			                                  headers = {'Content-Type':'application/json'})
			                                                                                       
		self.assertEqual(res.status_code, 403)


if __name__ == '__main__':
	unittest.main()
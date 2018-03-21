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
			#creating tables
			#db.session.close()
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


	def test_user_login(self):
		""" tests a user can login """

		reg = self.app.post('/api/v2/auth/register', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(reg.status_code, 201)
		rev = self.app.post('/api/v2/auth/login', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(rev.status_code, 200)


	def tests_non_registered_user_login(self):
		""" test non registered users can be logged in """

		users_data = {'email': 'test@test.com', 'password': 'test1023'}
		reg = self.app.post('/api/v2/auth/login', data = json.dumps(users_data), content_type = 'application/json')
		self.assertEqual(reg.status_code, 401)  #unauthorized access

	def tests_user_resets_password(self):
		""" tests a registered user can reset-password """
		reg = self.app.post('/api/v2/auth/register', data = json.dumps(self.user_data), content_type = 'application/json')
		self.assertEqual(reg.status_code, 201)
		users_data = {'email':'demo@test.com', 'new_password': 'test1023'}
		res = self.app.post('/api/v2/auth/reset-password', data = json.dumps(users_data), content_type = 'application/json')
		self.assertEqual(res.status_code, 200)





if __name__ == '__main__':
	unittest.main()
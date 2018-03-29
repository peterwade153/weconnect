import sys
sys.path.append('..')
import json
import unittest
from app import app
from app.models import db


class WeconnectTestCase(unittest.TestCase):
	""" weconnect business test case """

	def setUp(self):
		self.app = app.test_client()
		app.testing = True
		self.business_data = {
		                      'business_name':'rokoltd',
		                      'category':'construction',
		                      'location':'kampala'
		                      }
		self.review_data = {
		                    'review':'Great services and wonderful customer care'
		                    }


		with app.app_context():
			# create tables
			db.drop_all()
			db.create_all()


	def register_user(self, username = 'demo', email = 'demo@test.com', password = 'demo12345'):
		""" func that registers a user """
		user_data = {'username': username,
		             'email': email,
		             'password': password
		            }
		return self.app.post('/api/v2/auth/register', data = json.dumps(user_data), content_type = 'application/json')

	def login_user(self, email = 'demo@test.com', password = 'demo12345'):
		""" func that logs in user """
		user_data = {'email': email,
		             'password': password
		             }
		return self.app.post('/api/v2/auth/login', data = json.dumps(user_data), content_type = 'application/json')


	def test_business_registration(self):
		""" tests a user can register a business """

		self.register_user()
		result = self.login_user()
		token = json.loads(result.data.decode())['token']
		reg = self.app.post('/api/v2/businesses', data = json.dumps(self.business_data),
		                                         headers = {'Content-Type':'application/json','Authorization':token})
			                                                                                        
		self.assertEqual(reg.status_code, 201)
		self.assertIn('registered successfully', str(reg.data))

	def test_business_already_registered(self):
		""" tests abusiness can be registered twice """

		self.register_user()
		res = self.login_user()
		token = json.loads(res.data.decode())['token']
		rev = self.app.post('/api/v2/businesses', data = json.dumps(self.business_data), 
			                                        headers = {'Content-Type':'application/json','Authorization':token})
			                                                                                        
		self.assertEqual(rev.status_code, 201)
		reg = self.app.post('/api/v2/businesses', data = json.dumps(self.business_data), 
			                                          headers = {'Content-Type':'application/json','Authorization':token})
			                                                                                        
		self.assertEqual(reg.status_code, 202)
		self.assertIn('Business registered already', str(reg.data))


	def test_invalid_data(self):
		""" tests invalid data is not allowed """

		self.register_user()
		res = self.login_user()
		token = json.loads(res.data.decode())['token']
		invalid_data = {'business_name':'@#$$ltd','location':'*&(empe','category':'*&^^)(ling'}
		rev = self.app.post('/api/v2/businesses', data = json.dumps(invalid_data), 
			                                         headers = {'Content-Type':'application/json','Authorization':token})
			                                                                                        
		self.assertEqual(rev.status_code, 403)


	def test_viewing_business(self):
		""" tests a user can view a business """

		self.register_user()
		res = self.login_user()
		token = json.loads(res.data.decode())['token']
		rev = self.app.post('/api/v2/businesses', data = json.dumps(self.business_data), 
			                                      headers = {'Content-Type':'application/json','Authorization':token})
			                                                                                        
		self.assertEqual(rev.status_code, 201)
		reg = self.app.get('/api/v2/businesses/1', headers = {'Content-Type':'application/json','Authorization':token})
		self.assertEqual(reg.status_code, 200)
			                                                                                        

	def test_editing_business(self):
		""" tests a user can edit a registered business """
		self.register_user()
		result = self.login_user()
		token = json.loads(result.data.decode())['token']
		reg = self.app.post('/api/v2/businesses', data = json.dumps(self.business_data), 
			                                     headers = {'Content-Type':'application/json','Authorization':token})
			                                                                                        
		self.assertEqual(reg.status_code, 201)
		new_business = {'new_name':'temboltd','location':'kawempe','category':'milling'}
		res = self.app.put('/api/v2/businesses/1', data = json.dumps(new_business), 
			                                     headers = {'Content-Type':'application/json','Authorization':token})
			                                                                                   
		self.assertEqual(res.status_code, 200)


	def test_deleting_business(self):
		""" tests a user can delete a registered business """

		self.register_user()
		reg = self.login_user()
		token = json.loads(reg.data.decode())['token']
		rev = self.app.post('/api/v2/businesses', data = json.dumps(self.business_data), 
			                                     headers = {'Content-Type':'application/json','Authorization':token})
			                                                                                        
		self.assertEqual(rev.status_code, 201)
		res = self.app.delete('/api/v2/businesses/1', headers = {'Content-Type':'application/json','Authorization':token})
		self.assertEqual(res.status_code, 200)                                                                                         


	def test_adding_review(self):
		""" tests a user can review a business """

		self.register_user()
		reg = self.login_user()
		token = json.loads(reg.data.decode())['token']
		rev = self.app.post('/api/v2/businesses', data = json.dumps(self.business_data), 
			                                     headers = {'Content-Type':'application/json','Authorization':token})
			                                                                                        
		self.assertEqual(rev.status_code, 201)
		result = self.app.post('/api/v2/businesses/1/reviews', data = json.dumps(self.review_data), 
			                                     headers = {'Content-Type':'application/json','Authorization':token}) 
			                                                                                                    
		self.assertEqual(result.status_code, 201)

	def test_invalid_review_data(self):
		""" tests invalid review data is not acceppted """

		self.register_user()
		reg = self.login_user()
		token = json.loads(reg.data.decode())['token']
		rev = self.app.post('/api/v2/businesses', data = json.dumps(self.business_data), 
			                                    headers = {'Content-Type':'application/json','Authorization':token})
			                                                                                        
		self.assertEqual(rev.status_code, 201)
		review = {'review':' #$Great services and wonderful customer care'}
		result = self.app.post('/api/v2/businesses/1/reviews', data = json.dumps( review ), 
			                                       headers = {'Content-Type':'application/json','Authorization':token})
			                                                                                                     
		self.assertEqual(result.status_code, 403)



	def test_viewing_business_reviews(self):
		""" tests a user can view business reviews """

		self.register_user()
		reg = self.login_user()
		token = json.loads(reg.data.decode())['token']
		rev = self.app.post('/api/v2/businesses', data = json.dumps(self.business_data), 
			                                    headers = {'Content-Type':'application/json','Authorization':token})
			                                                                                        
		self.assertEqual(rev.status_code, 201)
		result = self.app.post('/api/v2/businesses/1/reviews', data = json.dumps(self.review_data), 
			                                     headers = {'Content-Type':'application/json','Authorization':token}) 
			                                                                                                    
		self.assertEqual(result.status_code, 201)

		review = self.app.get('/api/v2/businesses/1/reviews', 
			                                     headers = {'Content-Type':'application/json','Authorization':token}) 
		self.assertEqual(review.status_code, 200)
			                                                 


if __name__ == '__main__':
	unittest.main()
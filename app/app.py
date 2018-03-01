import sys
sys.path.append('..')
import re
import json
from flask import Flask, request, session, jsonify, make_response, render_template
from classes.user import User

app = Flask(__name__)

app.secret_key = 'younoscretet'

''' creating an instance of the user '''
user = User()

''' dictionary to store our users'''
users = {}


@app.route('/')
def display_documentation():
	""" route displays api documentation """

	return render_template('index.html')


@app.route('/api/v1/auth/register', methods = ['POST'])
def register():
	""" route enables a user to register """

	data = request.get_json()

	username = data['username']
	name_match = re.match('([A-Za-z0-9])', username)
	password = data['password']
	password_match = re.match('([A-Za-z0-9]{4,})', password)

	if name_match and password_match:
		''' checking if user is not already registered '''
		if username not in users.keys():
			users[username] = password
			return jsonify({'success': True,
							'message': 'Registered successfully',
				             'data': {'Username': username}
				             }), 201

		return jsonify({'success': False,
			            'message': 'User already registered!'}), 202
	else:
		return jsonify({'success': False,
			            'message': 'Your password should be atleast 4 characters, no special characters'}),403

@app.route('/api/v1/auth/login', methods = ['POST'])
def login():
	""" route enables a user to login """

	data = request.get_json()

	username = data['username']
	name_match = re.match('([A-Za-z0-9])', username)
	password = data['password']
	password_match = re.match('([A-Za-z0-9]{4,})', password)

	if name_match and password_match:

		#if check_password_hash(users[username], password):
		if ( username, password ) in users.items():
			''' checking user is already registered '''
			session['logged_in'] = True
			return jsonify({'success': True,
				            'message': 'Logged in successfully!'}), 200
		return jsonify({'message': 'Username and password dont match'}), 401
	else:
		return jsonify({'success': False, 
			            'message':'Username and password should atleast be 4 characters or digits'}),400


@app.route('/api/v1/auth/logout', methods = ['POST'])
def logout():
	""" route for logging out alogged in user """

	session.pop('logged_in', None)
	return jsonify({'success': True,
		            'message': 'Logged out'}), 200


@app.route('/api/v1/auth/reset-password', methods = ['POST'])
def reset_password():
	""" route enables user reset their password """

	data = request.get_json()
	
	''' check if user is already registered here'''
	username = data['username']
	name_match = re.match('([A-Za-z0-9]{4,})', username)
	password = data['password']
	password_match = re.match('([A-Za-z0-9]{4,})', password)
	new_password = data['new_password']
	new_password_match = re.match('([A-Za-z0-9]{4,})', new_password)

	if name_match and password_match and new_password_match:
		if ( username, password ) in users.items():
			users['username'] = password
			return jsonify({'success':True,
				            'message': 'password reset successfully!'}), 200

		return jsonify({'success':True,
			            'message': 'user not registered here!'}), 404

	return jsonify({'success': False,
		            'message':'username and password atleast 4 characters or digits'}), 400


@app.route('/api/v1/businesses', methods = ['POST', 'GET'])
def business():
	""" route enables user register a business and view businesses"""

	if request.method == 'POST':
		""" registering new business"""

		data = request.get_json()
		name = data['business_name']
		business_match = re.match('([A-Za-z0-9])', name)
		if business_match:
			business = user.register_business(name)
			return jsonify({'success':True,
				            'Business registered successfully': business }), 201

		return jsonify({'success':False,
			            'message': 'Business_name should be characters or digits'}), 400
 
	else:
		# GET
		""" return registered businesses """

		my_businesses = user.view_registered_businesses()
		if not my_businesses:
			return jsonify({'success': False,
				            'message': 'no business registered'}), 404

		return jsonify({'success': True,
			            'businesses': my_businesses}), 200


@app.route('/api/v1/businesses/<id>', methods = ['PUT', 'GET', 'DELETE'])
def update_get_delete_business(id):
	""" route allows a user update Delete and get a registered business """

	if request.method == "PUT":
		""" Update  a registered business """

		data = request.get_json()
		name = data['new_name']
		name_match = re.match('([A-Za-z0-9])', name)
		if name_match:
			update = user.update_registered_business(int(id), data['new_name'])
			if update:
				return jsonify({'success':True,
					            'Business updated to': update}), 200

			return jsonify({'Success':False,
				            'message': 'Business not registered here!'}), 404

		return jsonify({'success': False,
		                'message': 'New name should be characters or digits'}), 400


	elif request.method == "DELETE":
		""" deletes a registered business """

		business = user.delete_registered_business(int(id))
		if not business:
			return jsonify({'success': False,
				            'message': 'business not registered here'}), 404

		return jsonify({'success': True,
			            'message': 'Business deleted successfully'}), 200

	else:
		""" enable user view a registered business """

		business = user.view_a_business(int(id))
		if not business:
			return jsonify({'success': False,
				            'message': 'Business not registered here'}), 404

		return jsonify({'success': True,
		                'Business': business}),200



@app.route('/api/v1/businesses/<business_id>/reviews', methods = ['POST', 'GET'])
def review_and_view_business_reviews(business_id):
	""" route allows user to review and view its reviews business """

	if request.method == 'POST':
		""" method to add review"""
		data = request.get_json()
		reviews = data['review']
		reviews_match = re.match('([A-Za-z0-9])', reviews)
		if reviews_match:
			my_review = user.add_review(int(business_id), data['review'])
			if my_review:
				return jsonify({'success': True,
					            'message': 'Review added successfully!'}), 201

			return jsonify({'success': False,
				            'message':'business not registered here'}), 404

		return jsonify({'success': False,
			            'message': 'Review should have only charaters and digits'}), 403

	#GET
	else:
		business = user.view_business_reviews(int(business_id))
		if business:
			return jsonify({'success': True,
				            'reviews': business}), 200

		return jsonify({'success': False,
			            'message':'No reviews registered yet or Business not registered'}), 404


if __name__ == '__main__':
	app.run(debug = True)


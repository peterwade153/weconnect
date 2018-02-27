import sys
sys.path.append('..')
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
	if not data['username'] and not data['password']:
		return make_response(jsonify({'message': 'please fill in username and password'})), 403
	#stripping off any leading and tailing whitespaces both password and username
	username = data['username']
	username.strip()  
	password = data['password']
	password.strip()   

	''' checking if user is not already registered '''
	if username not in users.keys():
		users[username] = password
		return make_response(jsonify({'message': 'registered successfully'})), 201
	return make_response(jsonify({'message': 'user already exists, please choose another username'})), 202


@app.route('/api/v1/auth/login', methods = ['POST'])
def login():
	""" route enables a user to login """

	data = request.get_json()
	if not data['username'] and not data['password']:
		return make_response(jsonify({'message': 'please fill in username and password'})), 403

	username = data['username']
	username.strip()
	password = data['password']
	password.strip()

	''' checking user is already registered '''
	if username in users.keys() and password in users.values():
		session['logged_in'] = True
		return make_response(jsonify({'message': 'logged in successfully!'})), 200

	return make_response(jsonify({'message': 'username and password dont match'})), 404


@app.route('/api/v1/auth/logout', methods = ['POST'])
def logout():
	""" route for logging out alogged in user """

	session.pop('logged_in', None)
	return jsonify({'message': 'successfully logged out'}), 200


@app.route('/api/v1/auth/reset-password', methods = ['POST'])
def reset_password():
	""" route enables user reset their password """

	data = request.get_json()
	
	''' check if user is already registered here'''
	username = data['username']
	username.strip()
	password = data['password']
	password.strip()
	new_password = data['new_password']
	new_password.strip()
    
    #check if passed username and password mat
	if ( username, password ) in users.items():
		users['username'] = new_password
		return jsonify({'message': 'password reset successfully!'}), 200

	return jsonify({'message': 'user not registered here!'}), 404

	#return jsonify({'message': 'please fill in username and password'}), 403


@app.route('/api/v1/businesses', methods = ['POST', 'GET'])
def business():
	""" route enables user register a business and view businesses"""

	if request.method == 'POST':
		""" registering new business"""

		data = request.get_json()
		if data['business_name']:
			business = user.register_business(data['business_name'])
			return jsonify({'Business registered': business }), 201

		return jsonify({'message': 'please fill in business_name'}), 400

	else:
		# GET
		""" return registered businesses """

		my_businesses = user.view_registered_businesses()
		if not my_businesses:
			return jsonify({'message': 'no business registered'}), 404

		return jsonify({'businesses': my_businesses}), 200


@app.route('/api/v1/businesses/<business_id>', methods = ['PUT', 'GET', 'DELETE'])
def update_get_delete_business(business_id):
	""" route allows a user update Delete and get a registered business """

	if request.method == 'PUT':
		""" Update  a registered business """

		data = request.get_json()
		if data['new_name']:
			if user.update_registered_business(business_id, data['new_name']):
				return jsonify({'message': 'Business updated successfully!'}), 200

			return jsonify({'message': 'Business not registered here!'}), 404

		return jsonify({'message': 'please fill new_name'}), 400

	elif request.method == 'DELETE':
		""" deletes a registered business """

		business = user.delete_registered_business(business_id)
		if not business:
			return jsonify({'message': 'business not registered here'}), 404

		return jsonify({'message': 'Business deleted successfully'}), 200

	else:
		""" enable user view a registered business """

		business = user.view_a_business(business_id)
		if not business:
			return jsonify({'message': 'Business not registered here'}), 404

		return jsonify({'Business': business}),200



@app.route('/api/v1/businesses/<business_id>/reviews', methods = ['POST', 'GET'])
def review_and_view_business_reviews(business_id):
	""" route allows user to review and view its reviews business """

	if request.method == 'POST':
		""" method to add review"""
		data = request.get_json()
		if data['review']:
			my_review = user.add_review(business_id, data['review'])
			if my_review:
				return jsonify({'message': 'Review added successfully!'}), 201

			return jsonify({'message':'business not registered here'}), 404

		return jsonify({'message': 'please enter review'}), 403

	else:
		business = user.view_business_reviews(business_id)
		if business:
			return jsonify({'reviews': business}), 200

		return jsonify({'message':'no reviews registered yet'}), 404


if __name__ == '__main__':
	app.run(debug = True)


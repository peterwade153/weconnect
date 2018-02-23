import sys
sys.path.append('..')
import json
from flask import Flask, request, session, jsonify, make_response
from classes.user import User

app = Flask(__name__)

app.secret_key = 'younoscretet'

''' creating an instance of the user '''
user = User()

''' dictionary to store our users'''
users = {}

@app.route('/api/v1/auth/register', methods = ['POST'])
def register():
	""" route enables a user to register """

	data = request.get_json()
	if not data['username'] and not data['password']:
		return make_response(jsonify({'message': 'please fill in username and password'})), 400
	username = data['username']
	password = data['password']

	''' checking if user is not already registered '''
	if username not in users.keys():
		users[username] = password
		return make_response(jsonify({'message': 'registered successfully'})), 201
	return make_response(jsonify({'message': 'user already registered'})), 202


@app.route('/api/v1/auth/login', methods = ['POST'])
def login():
	""" route enables a user to login """

	data = request.get_json()
	if not data['username'] and not data['password']:
		return make_response(jsonify({'message': 'please fill in username and password'})), 400

	username = data['username']
	password = data['password']

	''' checking user is already registered '''
	if username in users.keys() and password in users.values():
		session['logged_in'] = True
		return make_response(jsonify({'message': 'logged in successfully!'})), 200

	return make_response(jsonify({'message': 'please register to login'})), 401


@app.route('/api/v1/auth/logout', methods = ['POST'])
def logout():
	""" route for logging out alogged in user """

	session.pop('logged_in', None)
	return jsonify({'message': 'successfully logged out'}), 200


@app.route('/api/v1/auth/reset-password', methods = ['POST'])
def reset_password():
	""" route enables user reset their password """

	data = request.get_json()
	if data['username'] and data['new_password']:
		''' check if user is already registered here'''
		if data['username'] in users.keys():
			users['username'] = data['new_password']
			return jsonify({'message': 'password reset successfully!'}), 200

		return jsonify({'message': 'user not registered here!'}), 404

	return jsonify({'message': 'please fill in username and password'}), 403


@app.route('/api/v1/businesses', methods = ['POST'])
def register_business():
	""" route enables user registera business"""

	data = request.get_json()
	if data['id'] and data['business_name']:
		business = user.register_business(data['id'], data['business_name'])
		if business:
			return jsonify({'message': 'Business registered successfully'}), 201

		return jsonify({'message': 'business registered already'})

	return jsonify({'message': 'please fill in business id and business_name'}), 403



@app.route('/api/v1/businesses/<business_id>', methods = ['PUT'])
def update_business(business_id):
	""" route allows a user update a business """

	data = request.get_json()
	if data['new_name']:
		user.update_registered_business(business_id, data['new_name'])
		return jsonify({'message': 'Business updated successfully!'}), 200

	return jsonify({'message': 'please fill in id and new_name'}), 403


@app.route('/api/v1/businesses/<business_id>', methods = ['DELETE'])
def delete_business(business_id):
	""" route should enable a user delete a registered business """

	business = user.delete_registered_business(business_id)
	if not business:
		return jsonify({'message': 'business not registered here'}), 404

	return jsonify({'message': 'Business deleted successfully'}), 200


@app.route('/api/v1/businesses', methods = ['GET'])
def view_businesses():
	""" route returns all businesses """

	my_list = user.view_registered_businesses()
	if not my_list:
		return jsonify({'message': 'no business registered'}), 404

	return jsonify({'businesses': my_list}), 200


@app.route('/api/v1/businesses/<business_id>', methods = ['GET'])
def view_business(business_id):
	""" route returns a business by id"""

	business = user.view_a_business(business_id)
	if not business:
		return jsonify({'message': 'Business not registered here'}), 404

	return jsonify({'Business': business})


@app.route('/api/v1/businesses/<business_id>/reviews', methods = ['POST'])
def review_business(business_id):
	""" route allows user to review a business """

	data = request.get_json()
	if data['review']:
		my_review = user.add_review(business_id, data['review'])
		if my_review:
			return jsonify({'message': 'Review added successfully!'}), 201

		return jsonify({'message':'business not registered here'}), 404

	return jsonify({'message': 'please enter review'}), 403


@app.route('/api/v1/businesses/<business_id>/reviews', methods = ['GET'])
def view_business_reviews(business_id):
	""" route enables user see business reviews """

	business = user.view_business_reviews(business_id)
	if business:
		return jsonify({'reviews': business }), 200

	return jsonify({'messages': 'no reviews registered yet'}), 404




if __name__ == '__main__':
	app.run(debug = True)


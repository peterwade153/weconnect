import sys
sys.path.append('..')
import json
from flask import Flask, request, jsonify, make_response
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
		return make_response(jsonify({'message': 'please fill in username and password'})),403

	username = data['username']
	password = data['password']

	''' checking if user is not already registered '''
	if username not in users.keys():
		users['username'] = password
		return make_response(jsonify({'message': 'registered successfully'})),201

	return make_response(jsonify({'message': 'user already registered'})),202


@app.route('/api/v1/auth/login', methods = ['POST'])
def login():
	""" route enables a user to login """

	data = request.get_json()
	if not data['username'] and not data['password']:
		return make_response(jsonify({'message': 'please fill in username and password'}))

	username = data['username']
	password = data['password']

	''' checking user is already registered if not they shud register'''
	if username not in users.keys() and password not in users.values():
		return make_response(jsonify({'message': 'please register to login'}))

	session['logged_in'] = True
	return make_response(jsonify({'message': 'logged in successfully!'}))


if __name__ == '__main__':
	app.run(debug = True)
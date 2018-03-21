""" authentication blueprint """

import os
import re
from flask import Blueprint, jsonify, request
import jwt
import datetime
from werkzeug.security import  check_password_hash, generate_password_hash
from app import app
from app.models import db, User



auth = Blueprint('auth', __name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')


@app.route('/api/v2/auth/register', methods = ['POST'])
def register_user():
	""" route registers a user """

	data = request.get_json()
	name_match = re.match('^[A-Za-z0-9]+$', data['username'])
	email_match = re.match('^[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+$', data['email'])
	password_match = re.match('^[A-Za-z0-9]{4,}$', data['password'])

	if name_match and email_match and password_match:

		user = User.query.filter_by(email = data['email']).first()         #check if user is not registered already
		if not user:
			new_user = User(username = data['username'], email =  data['email'], password = data['password'])
			db.session.add(new_user)
			db.session.commit()
			return jsonify({'message':'Successfully registered',
			                'success': True
			                }), 201
		return jsonify({'message':'User already registered, Login',
			            'success': False}), 202

	return jsonify({'message':'Please all fields are required, should be characters or digits and email should be valid!',
		            'success': False}), 403


@app.route('/api/v2/auth/login', methods = ['POST'])
def login_user():
	""" route logs in registered user """

	data = request.get_json()
	email_match = re.match('^[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+$', data['email'])
	password_match = re.match('^[A-Za-z0-9]{4,}$', data['password'])

	if email_match and password_match:
		user = User.query.filter_by(email = data['email']).first()
		if user:
			if check_password_hash(user.password, data['password']):
				payload = {
				           'exp':datetime.datetime.utcnow() + datetime.timedelta(hours = 10) ,
				           'iat':datetime.datetime.utcnow(),
				           'sub':user.id }

				token = jwt.encode(
					               payload, 
					               app.config['SECRET_KEY'], 
					               algorithm = 'HS256') 

				return jsonify({'message':'Logged in successfully',
					            'success': True,
					            'token': token.decode('UTF-8')}),200

			return jsonify({'message':'An error occured,please try again!',
				            'success': False}), 401

		return jsonify({'message':'User not registered, please register!',
			            'success': False}), 401

	return jsonify({'message':'Please all fields are required, should be characters or digits',
		            'success': False}), 403



@app.route('/api/v2/auth/reset-password', methods = ['POST'])
def reset_password():
	""" route enables user reset-password """

	data = request.get_json()
	email_match = re.match('^[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+$', data['email'])
	new_password_match = re.match('^[A-Za-z0-9]{4,}$', data['new_password'])

	if  email_match and new_password_match:

		user = User.query.filter_by( email = data['email']).first()
		if user:
			user.password = generate_password_hash(data['new_password'], method='sha256')
			db.session.commit()
			return jsonify({'message': 'Password reset successfully',
				            'success': True}), 200

		return jsonify({'message':'An error occurred, check and try again!',
			            'success': False}), 403

	return jsonify({'message':'Please all fields are required, should be characters or digits and email should be valid!',
		            'success': False}), 403

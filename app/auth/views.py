""" authentication blueprint """

import os
import re
import jwt
import datetime
from werkzeug.security import  check_password_hash, generate_password_hash
from flask import Blueprint, jsonify, request
from app import app
from app.models import db, User


auth = Blueprint('auth', __name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')


@app.route('/api/v2/auth/register', methods=['POST'])
def register_user():
	""" route registers a user """

	data = request.get_json()

	valid_name = re.match('^[A-Za-z0-9]{,100}$', data['username'])
	valid_email = re.match('^[A-Za-z0-9.]+@[A-Za-z0-9]+\.[A-Za-z0-9.]{,100}$', data['email'])
	valid_password = re.match('^[A-Za-z0-9]{4,}$', data['password'])

	#if the data passes our validity check
	if valid_name and valid_email and valid_password:  

		user = User.query.filter_by(email=data['email']).first()         
		if not user:

			new_user = User(username=data['username'],
			                email=data['email'],
			                password=data['password'])
			db.session.add(new_user)
			db.session.commit()
			return jsonify({'Message':'Successfully registered',
			                'Status': 'Success'
			                }), 201

		return jsonify({'Message':'User already registered, Login',
			            'Status': 'Failed'}), 202

	return jsonify(
		{
		  'Message':'All fields required, Valid Email and Password  atleast 4 characters!',
		  'Status': 'Failed'
		}), 403


@app.route('/api/v2/auth/login', methods=['POST'])
def login_user():
	""" route logs in registered user """

	data = request.get_json()

	#validity check on the data using regular expressions
	email = re.match('^[A-Za-z0-9.]+@[A-Za-z0-9]+\.[A-Za-z0-9.]{,100}$',data['email'])
	password = re.match('^[A-Za-z0-9]{4,}$', data['password'])

	#if the data passes our validity check
	if email and password:
		user = User.query.filter_by(email=data['email']).first()

		if not user:

			return jsonify({'Message':'User not registered, please register!',
				            'Status': 'Failed'}), 401
		else:

			if check_password_hash(user.password, data['password']):
				payload = {
				           'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=2),
				           'iat':datetime.datetime.utcnow(),
				           'sub':user.id }

				token = jwt.encode(
					               payload, 
					               app.config['SECRET_KEY'], 
					               algorithm='HS256') 

				return jsonify({'Message':'Logged in successfully',
					            'Status':'Success',
					            'Token':token.decode('UTF-8')}),200

			return jsonify({'Message':'An error occured,please try again!',
				            'Status':'Failed'}), 401

	return jsonify(
		{
		'Message':'All fields are required,Valid Email and Password atleast 4 characters!',
		'Success':'Failed'
		}), 403





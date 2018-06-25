""" authentication blueprint """ 

import os
import re
import jwt
import datetime
from werkzeug.security import  check_password_hash, generate_password_hash
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from app import app
from app.models import db, User


auth = Blueprint('auth', __name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')


@app.route('/api/v2/auth/register', methods=['POST'])
def register_user():
	""" route registers a user """

	data = request.get_json()

	is_valid_name = re.match('^[A-Za-z0-9]{,100}$', data['username'])
	is_valid_email = re.match('^[A-Za-z0-9.]+@[A-Za-z0-9]+\.[A-Za-z0-9.]{,100}$',
	                                                           data['email'])
	is_valid_password = re.match('^[A-Za-z0-9]{4,}$', data['password'])

	#check if data passes the validity check
	if not (is_valid_password and is_valid_email):
		return jsonify({'Message':'All fields required, valid email and'+ 
		'Password should atleast be 4 characters!',
		                'Status':'Failed'}), 403

	user = User.query.filter_by(email=data['email']).first()         
	if user is not None:
		return jsonify({'Message':'User already registered, Login',
			            'Status':'Failed'}), 202

	new_user = User(username=data['username'],
		            email=data['email'],
		            password=data['password'])
	db.session.add(new_user)
	db.session.commit()
	return jsonify({'Message':'Successfully registered',
			        'Status':'Success'}), 201

@app.route('/api/v2/auth/login', methods=['POST'])
def login_user():
	""" route logs in registered user """

	data = request.get_json()
	#check if all fields are filled in
	if 'password' not in data.keys():
		return jsonify({'Message':'Password required',
		                'Success':'Failed'}), 403

	is_valid_email = re.match('^[A-Za-z0-9.]+@[A-Za-z0-9]+\.[A-Za-z0-9.]{,100}$',
		                                                     data['email'])
	is_valid_password = re.match('^[A-Za-z0-9]{4,}$', data['password'])

	#if the data passes our validity check
	if not is_valid_email and not is_valid_password:
		return jsonify({
		'Message':'Invalid Email or Password should be atleast 4 characters!',
		'Success':'Failed'}), 403

	user = User.query.filter_by(email=data['email']).first()
	if user is None:
		return jsonify({'Message':'User not registered, please register!',
				        'Status':'Failed'}), 401

	if not check_password_hash(user.password, data['password']):
		return jsonify({'Message':'An error occured,please try again!',
				        'Status':'Failed'}), 401
	#if password matches, then generate token for the user	
	payload = {'exp':datetime.datetime.utcnow()+ datetime.timedelta(hours=2),
	           'iat':datetime.datetime.utcnow(),
	           'sub':user.id}
	token = jwt.encode( payload,
		              app.config['SECRET_KEY'],
		              algorithm='HS256')

	return jsonify({'Message':'Logged in successfully',
				    'Status':'Success',
					'user_id': user.id,
				    'Token':token.decode('UTF-8')}), 200

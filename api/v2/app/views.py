import os
import jwt
from functools import wraps
from werkzeug.security import generate_password_hash
from flask import jsonify, request
from app import app
from app.models import db, User, Business, Review, BlacklistToken
from app.auth.views import auth


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db.init_app(app) #connecting sqlalchemy object to the app


def token_required(f):
	""" checking for the authentication token """

	@wraps(f)
	def decorate(*args, **kwargs):
		token = None
		if Authorization in request.headers:
			token = request.headers['Authorization']

		if not token:
			return jsonify({'message': 'Token is missing!'}), 403

		#check if token is blacklisted
		result = BlacklistToken.query.filter_by(token = token).first()
		if result:
			return jsonify({'message': 'Expired token, Login again'}), 403

		try:
			payload = jwt.decode(token, app.config['SECRET_KEY'])
			current_user = payload['sub']

		except jwt.ExpiredSignatureError:
			return jsonify ({'message': 'Expired token!'}), 403

		except jwt.InvalidTokenError:
			return jsonify({'message': 'Invalid token!'}), 403

		return f(current_user, *args, **kwargs)

	return decorate



@app.route('/api/v2/auth/logout', methods = ['POST'])
def logout():
	""" route logs out a logged in user """
	if 'Authorization' in request.headers:
		token = request.headers['Authorization']

	result = BlacklistToken.query.filter_by(token = token).first()
	if result:
		# if token is blacklisted, then user is already logged out

		return jsonify({'message': 'Logged out already',
			            'success': False}), 403

	else:
		#blacklist token

		blacklist = BlacklistToken(token = token)
		db.session.add(blacklist)
		db.session.commit()
		return jsonify({'success': True,
			           'message': 'Logged out successfully'}), 200

	return jsonify({'success': False,
		            'message': 'authentication token required'})



@app.route('/api/v2/auth/reset-password', methods = ['POST'])
@token_required
def reset_password(current_user):
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


@app.route('/api/v2/businesses' , methods = ['POST', 'GET'])
def businesses():
	""" route allows user register a business and view all registered businesses """
	return

@app.route('/api/v2/businesses/<id>', methods = ['GET', 'PUT', 'DELETE'])
def business():
	""" route allows user to get, update and delete a business """
	return

@app.route('/api/v2/businesses/<id>/reviews', methods = ['POST', 'GET'])
def reviews():
	""" route allows user review a a business """
	return
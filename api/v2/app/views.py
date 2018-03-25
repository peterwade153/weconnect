import os
import re
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
		if 'Authorization' in request.headers:
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
		            'message': 'authentication token required'}), 403



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
			if user.id == current_user:   #check if its account owner requesting password reset
				user.password = generate_password_hash(data['new_password'], method='sha256')
				db.session.commit()
				return jsonify({'message': 'Password reset successfully',
				                'success': True}), 200

			return jsonify({'message': 'Action failed',
				            'success': False}), 403

		return jsonify({'message':'An error occurred, check and try again!',
			            'success': False}), 403

	return jsonify({'message':'Please all fields are required, should be characters or digits and email should be valid!',
		            'success': False}), 403


@app.route('/api/v2/businesses' , methods = ['POST', 'GET'])
@token_required
def businesses(current_user):
	""" route allows user register a business and view all registered businesses """

	if request.method == 'POST':
		''' registering new business '''
		data = request.get_json()
		name_match = re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', data['business_name'])
		category_match = re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', data['category'])
		location_match = re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', data['location'])

		if name_match and category_match and location_match:
			biz = Business.query.filter_by(business_name = data['business_name']).first()
			if not biz:    #business nnot already registered

				new_biz = Business(business_name = data['business_name'], category = data['category'],
					                                                      location = data['location'],
					                                                      user_id = current_user)
				db.session.add(new_biz)
				db.session.commit()
				return jsonify({'success': True,
					            'message':'Business '+ data['business_name']+' registered successfully'}), 201

			# business registered already
			return jsonify({'success': False,
				            'message': 'Business registered already'}), 202

		return jsonify({'success':False,
			            'message': 'Only characters and digits are expected!'}), 403

	else:   
		# GET viewing businesses
		businesses = Business.query.all()
		if not businesses:
			return jsonify({'success': False,
				            'message': 'No business found'}), 404
		else:
			business_list = []
			for business in businesses:
				business_info = {}
				business_info['id'] = business.id
				business_info['business_name'] = business.business_name
				business_info['category'] = business.category
				business_info['location'] = business.location

				business_list.append(business_info)

			return jsonify({'Success': True,
				            'Business': business_list}), 200



@app.route('/api/v2/businesses/<id>', methods = ['GET', 'PUT', 'DELETE'])
@token_required
def business(current_user, id):
	""" route allows user to get, update and delete a business """

	if request.method == 'GET':
		''' allows user view a business '''

		business = Business.query.filter_by(id = id).first()
		if business:
			business_info = {}
			business_info['id'] = business.id
			business_info['business_name'] = business.business_name
			business_info['category'] = business.category
			business_info['location'] = business.location
			business_info['created_on'] = business.created_on
			business_info['modified_on'] = business.modified_on

			return jsonify({'success': True,
			                'business': business_info}), 200

		return jsonify({'success': False,
			            'message':'No business found'}), 404


	elif request.method == 'PUT':
		''' method only allows business owner to edit it '''

		data = request.get_json()
		name_match = re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', data['business_name'])
		category_match = re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', data['category'])
		location_match = re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', data['location'])

		if name_match and category_match and location_match:

			business = Business.query.filter_by(id = id).first()
			if business:
				if business.user_id == current_user:
					business.business_name = data['business_name']
					business.category = data['category']
					business.location = data['location']
					db.session.commit()

					return jsonify({'success': True,
						            'message': 'Business Updated successfully'}), 200

				return jsonify({'success': False,
					            'message': 'You dont have permission to perform this action!'}), 403

			return jsonify({'success': False,
				            'message':'No business found'}), 404

		return jsonify({'success':False,
			            'message': 'Only characters and digits are expected!'}), 403

	else:
		# delete business

		business = Business.query.filter_by(id = id).first()
		if business:
			if business.user_id == current_user:
				db.session.delete(business)
				db.session.commit()

				return jsonify({'success': True,
					            'message': 'Business deleted successfully'}), 200

			return jsonify({'success': False,
				            'message':'You dont have permission to perform this action!'}), 403

		return jsonify({'success': False,
			            'message': 'No business found!'}), 404


	

@app.route('/api/v2/businesses/<id>/reviews', methods = ['POST', 'GET'])
@token_required
def reviews(current_user, id):
	""" route allows user review a a business """

	if request.method == 'POST':
		''' Reviewing a business '''
		data = request.get_json()
		review_match = re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', data['review'])

		if review_match:
			result = Business.query.filter_by(id = id).first()

			if result:
				new_review = Review( review = data['review'], business_id = id)
				db.session.add(new_review)
				db.session.commit()
				return jsonify({'success': True,
					            'message': 'Review has been successfully added!'}), 201

			return jsonify({'success': False,
				            'message':'Business not registered here!'}), 404

		return jsonify({'success':False,
			            'message': 'Only characters and digits are expected!'}), 403


	else:
		''' Get request '''
		reviews = Review.query.filter_by(business_id = id).all()
		if reviews:
			review_list = []
			for review in reviews:
				review_info = {}
				review_info['review'] = review.review
				review_info['id'] = review.id

				review_list.append(review_info)

			return jsonify({'success': True,
					        'Review': review_list}), 200

		return jsonify({'success': False,
			            'message':'No reviews found!'}), 404



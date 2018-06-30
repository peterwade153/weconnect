import os
import re
import jwt
from functools import wraps
from flask import jsonify, request, render_template
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from app import app
from app.auth.views import auth
from app.models import db, User, Business, Review, ExpiredToken



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

#connecting sqlalchemy object to the app
db.init_app(app) 
#enables CORS
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/')
def display_documentation():
	""" route displays api documentation """

	return render_template('index.html')


def token_required(f):
	""" checking for the authentication token """

	@wraps(f)
	def decorate(*args, **kwargs):
		token = None
		if 'Authorization' in request.headers:
			token = request.headers['Authorization']

		if not token:
			return jsonify({'Message':'Token is missing!'}), 403

		#check if token is blacklisted
		expired_token = ExpiredToken.query.filter_by(token=token).first()

		if expired_token:
			return jsonify({'Message':'Expired token, Login again'}), 403

		try:
			payload = jwt.decode(token, app.config['SECRET_KEY'])
			current_user = payload['sub']

		except jwt.ExpiredSignatureError:
			return jsonify({'Message':'Expired token!'}), 403

		except jwt.InvalidTokenError:
			return jsonify({'Message':'Invalid token!'}), 403

		return f(current_user, *args, **kwargs)

	return decorate


@app.route('/api/v2/auth/logout', methods=['POST'])
def logout():
	""" route logs out a logged in user """

	if 'Authorization' not in request.headers:

		return jsonify({'Message':'Authentication token required',
		                'Status':'Failed'}), 403

	token = request.headers['Authorization']

	expired_token = ExpiredToken.query.filter_by(token=token).first()

	if expired_token is not None:
		return jsonify({'Message':'Logged out already',
			            'Status':'Failed'}), 403

	new_expired_token = ExpiredToken(token=token)
	db.session.add(new_expired_token)
	db.session.commit()
	return jsonify({'Message':'Logged out successfully',
			        'Status':'Success'}), 200


@app.route('/api/v2/auth/reset-password', methods=['POST'])
@token_required
def reset_password(current_user):
	""" route enables user reset-password """

	data = request.get_json()

	is_valid_email = re.match('^[A-Za-z0-9.]+@[A-Za-z0-9]+\.[A-Za-z0-9.]+$',
		                                                      data['email'])
	is_valid_new_password = re.match('^[A-Za-z0-9]{4,}$', data['new_password'])

	if not (is_valid_email and is_valid_new_password):
		return jsonify({
		'Message':'Invalid Email or Password should atleast be 4 characters!',
		'Status':False}), 403

	#check if user exists
	user = User.query.filter_by(email=data['email']).first()
	if user is None:
		return jsonify({'Message':'An error occurred, check and try again!',
			            'Status':'Failed'}), 403
	#check if its account owner requesting password reset
	if user.id != current_user:
		return jsonify({'Message':'Action failed',
				        'Status':'Failed'}), 403

	user.password = generate_password_hash(data['new_password'], method='sha256')
	db.session.commit()
	return jsonify({'Message':'Password reset successfully',
				    'Status':'Success'}), 200



@app.route('/api/v2/businesses', methods=['POST', 'GET'])
@token_required
def businesses(current_user):
	""" route allows user register a business and view all registered businesses """

	if request.method == 'POST':
		''' registering new business '''
		data = request.get_json()

		is_valid_name = re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', 
			                                 data['business_name'])
		is_valid_category = re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', 
			                                  data['category'])
		is_valid_location = re.match('^[A-Za-z]+[A-Za-z0-9 ]+$',
		                                      data['location'])

		if not (is_valid_name and is_valid_category and is_valid_location):
			return jsonify({'Message':'Only characters and digits are expected!',
			                'Status':'Failed'}), 403
		
		biz_name = data['business_name'].lower()
		business = Business.query.filter_by(business_name=biz_name).first()

		if business is not None:
			return jsonify({'Message':'Business registered already',
				            'Status':'Failed'}), 202

		new_business = Business(business_name=data['business_name'],
				           category=data['category'],
				           location=data['location'],
				           user_id=current_user)
		db.session.add(new_business)
		db.session.commit()
		return jsonify({
		   'Message':data['business_name'].upper()+' Registered Successfully',
	       'Status':'Success'}), 201


	else :

		name = request.args.get('q', None)
		limit = request.args.get('limit', None, type = int)
		page = request.args.get('page', 1, type = int)
		location = request.args.get('location', None)
		category = request.args.get('category', None)


		if limit is not None:
			business_results = Business.query.paginate(page, limit, False)
			response = {
			     'Businesses':[i.business_object() 
			                             for i in business_results.items],
			     'pages':business_results.pages,
			     'next':business_results.next_num,
			     'current':business_results.page,
			     'prev':business_results.prev_num
			}

			return jsonify(response), 200

		elif name is not None:
			businesses = Business.query.filter(
				             Business.business_name.ilike('%'+name+'%'))
			business_list = [business.business_object() 
				                     for business in businesses]
			return jsonify({'Status':'Success',
				            'Businesses':business_list}), 200

		elif location is not None:
			businesses = Business.query.filter(
				             Business.location.ilike('%'+location+'%'))
			business_list = [business.business_object() 
				                     for business in businesses]
			return jsonify({'Status':'Success',
				            'Businesses':business_list}), 200
			
		elif category is not None:
			businesses = Business.query.filter(
				             Business.category.ilike('%'+category+'%'))
			business_list = [business.business_object() 
				                     for business in businesses]
			return jsonify({'Status':'Success',
				            'Businesses':business_list}), 200

		#GET without params
		businesses = Business.get_businesses()
		business_list = [business.business_object() 
				                     for business in businesses]

		return jsonify({'Status':'Success',
				            'Businesses':business_list}), 200


@app.route('/api/v2/businesses/<id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def business(current_user, id):
	""" route allows user to get, update and delete a business """

	if request.method == 'GET':
		''' allows user view a business '''
		business = Business.get_business(id)

		if business is None:

			return jsonify({'Status':'Failed',
			            'Message':'No business found'}), 404

		business_info = business.business_object()

		return jsonify({'Status':'Success',
			            'Business':business_info}), 200



	if request.method == 'PUT':
		''' method only allows business owner to edit it '''
		data = request.get_json()
		business = Business.get_business(id)
		if not business:
			return jsonify({'Status':'Failed',
				            'Message':'No business found'}), 404

		if 'business_name' in data.keys():
			is_valid_name = re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', 
					                                  data['business_name'])
			if not is_valid_name:
				return jsonify({'Status':'Failed',
		                   'Message':'characters or digits expected!'}), 403
			business.business_name = data['business_name']
		if 'category' in data.keys():
			is_valid_category = re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', 
					                                        data['category'])
			if not is_valid_category:
				return jsonify({'Status':'Failed',
		                    'Message':'characters or digits expected!'}), 403
			business.category = data['category']
		if 'location' in data.keys():
			is_valid_location = re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', 
					                                         data['location'])
			if not is_valid_location:
				return jsonify({'Status':'Failed',
		                        'Message':'characters or digits expected!'}), 403
			business.location = data['location']

		if business.user_id != current_user:
			return jsonify({'Status':'Failed',
				            'Message':'You are not permitted'}), 403
		#save new business details
		db.session.commit()
		return jsonify({'Status':'Success',
				        'Message':'Business Updated successfully'}), 200



	elif request.method == 'DELETE':
		""" deletes a business """

		business = Business.get_business(id)

		if business is None:
			return jsonify({'Status':'Failed',
			                'Message':'No business found!'}), 404

		if business.user_id != current_user:
			return jsonify({'Status':'Failed',
				            'Message':'You are not permitted'}), 403
		db.session.delete(business)
		db.session.commit()

		return jsonify({'Status':'Success',
					    'Message':'Business deleted successfully'}), 200


@app.route('/api/v2/businesses/<id>/reviews', methods=['POST','GET'])
@token_required
def reviews(current_user, id):
	""" route allows user review a a business """

	if request.method == 'POST':
		''' Reviewing a business '''
		data = request.get_json()

		is_valid_review = re.match('^[A-Za-z]+[A-Za-z0-9 ]{,200}$',
			                                             data['review'])

		#if the data passes our validity check
		if not is_valid_review:
			return jsonify({'Status':'Failed',
			  'Message':'Only characters and not beyond 200 charaters!'}), 403

		business = Business.get_business(id)
		if business is None:
			return jsonify({'Status':'Failed',
				            'Message':'Business not registered here!'}), 404

		new_review = Review(review=data['review'], business_id=id)
		db.session.add(new_review)
		db.session.commit()
		return jsonify({'Status':'Success',
					     'Message':'Review has been successfully added!'}), 201
						 
	elif request.method == 'GET':
		''' Get request '''
		reviews = Review.query.filter_by(business_id=id).all()
		author = User.query.filter_by(id=current_user).first()
		business = Business.get_business(id)

		review_list = []
		for review in reviews:
			review_info = {}
			review_info['review'] = review.review
			review_info['business_name'] = business.business_name
			review_info['reviewed_on'] = review.reviewed_on
			review_info['review_author'] = author.username

			review_list.append(review_info)

		return jsonify({'Status':'Success',
				        'Review':review_list}), 200

import os
import re
import jwt
from functools import wraps
from flask import jsonify, request
from werkzeug.security import generate_password_hash
from app import app
from app.auth.views import auth
from app.models import db, User, Business, Review, BlacklistToken



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

#connecting sqlalchemy object to the app
db.init_app(app) 


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
		blacklisted_token = BlacklistToken.query.filter_by(token=token).first()

		if blacklisted_token:
			return jsonify({'Message':'Expired token, Login again'}), 403

		try:
			payload=jwt.decode(token, app.config['SECRET_KEY'])
			current_user=payload['sub']

		except jwt.ExpiredSignatureError:
			return jsonify ({'Message':'Expired token!'}), 403

		except jwt.InvalidTokenError:
			return jsonify({'Message':'Invalid token!'}), 403

		return f(current_user, *args, **kwargs)

	return decorate



@app.route('/api/v2/auth/logout', methods=['POST'])
def logout():
	""" route logs out a logged in user """

	if 'Authorization' in request.headers:
		token=request.headers['Authorization']

	blacklisted_token = BlacklistToken.query.filter_by(token=token).first()

	if blacklisted_token:
		return jsonify({'Message':'Logged out already',
			            'Status':'Failed'}), 403

	else:	

		blacklist_token=BlacklistToken(token=token)
		db.session.add(blacklist_token)
		db.session.commit()
		return jsonify({'Message':'Logged out successfully',
			            'Status':'Success'}), 200

	return jsonify({'Message':'Authentication token required',
		            'Status':'Failed'}), 403



@app.route('/api/v2/auth/reset-password', methods=['POST'])
@token_required
def reset_password(current_user):
	""" route enables user reset-password """

	data=request.get_json()

	valid_email=re.match('^[A-Za-z0-9.]+@[A-Za-z0-9]+\.[A-Za-z0-9.]+$',data['email'])
	valid_new_password=re.match('^[A-Za-z0-9]{4,}$', data['new_password'])

	if valid_email and valid_new_password:

		user = User.query.filter_by(email=data['email']).first()
		if user:
			#check if its account owner requesting password reset
			if user.id==current_user:   
				user.password=generate_password_hash(data['new_password'],
				                                           method='sha256')
				db.session.commit()
				return jsonify({'Message':'Password reset successfully',
				                'Status':'Success'}), 200

			return jsonify({'Message':'Action failed',
				            'Status':'Failed'}), 403

		return jsonify({'Message':'An error occurred, check and try again!',
			            'Status':'Failed'}), 403

	return jsonify(
		{
		'Message':'Fill all fields, Valid Email and Password atleast 4 characters!',
		'Status': False
		}), 403


@app.route('/api/v2/businesses' , methods=['POST','GET'])
@token_required
def businesses(current_user):
	""" route allows user register a business and view all registered businesses """

	if request.method=='POST':
		''' registering new business '''
		data=request.get_json()

		valid_biz_name=re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', data['business_name'])
		valid_category=re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', data['category'])
		valid_location=re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', data['location'])

		if valid_biz_name and valid_category and valid_location:

			biz = Business.query.filter_by(business_name=data['business_name']).first()

			if not biz:
				new_biz = Business(business_name=data['business_name'],
				                   category=data['category'],
				                   location=data['location'],
				                   user_id=current_user)
				db.session.add(new_biz)
				db.session.commit()
				return jsonify(
					{
					'Message':data['business_name'].upper() +' Registered Successfully',
					'Status':'Success'
					}), 201

			# business registered already
			return jsonify({'Message':'Business registered already',
				            'Status':'Failed'}), 202

		return jsonify({'Message':'Only characters and digits are expected!',
			            'Status':'Failed'}), 403

	else:   
		# GET viewing businesses

		name=request.args.get('q', None)
		limit=request.args.get('limit', None, type = int)
		page=request.args.get('page', 1, type = int)
		location=request.args.get('location', None)
		category=request.args.get('category', None)

		if name:
			business_query = Business.query.filter(
				             Business.business_name.ilike('%'+name+'%'))
			if business_query:
				business_info=[business.business_object() for business in business_query]
				return jsonify({'Status': 'Success',
			                    'Business':business_info}), 200 

			return jsonify({'Status':'Failed',
				            'Message':'No business found'}), 404
		if limit:
			business_query = Business.query.paginate(page, limit, False)
			response={
			     'Businesses':[i.business_object() for i in business_query.items],
			     'pages': business_query.pages,
			     'next':business_query.next_num,
			     'current':business_query.page,
			     'prev':business_query.prev_num
			}

			return jsonify(response), 200

		if location:
			location_query = Business.query.filter(
				             Business.location.ilike('%'+location+'%'))
			if location_query:
				business_info = [i.business_object() for i in location_query]
				return jsonify({'success': True,
					            'business': business_info}), 200
			return jsonify({'success': False,
				            'message': 'No business found'}), 404

		if category:
			category_query = Business.query.filter_by(category=category).all()
			if category_query:
				business_info=[i.business_object() for i in category_query]
				return jsonify({'success': True,
					            'business': business_info}), 200
				
			return jsonify({'success':False,
				            'message':'No business found'}), 404


		else:
			businesses = Business.query.all()
			if not businesses:
				return jsonify({'Status':'Failed',
				                'Message':'No business found'}), 404
			else:
				business_list=[business.business_object() for business in businesses]

				return jsonify({'Status':'Success',
				                'Businesses': business_list}), 200



@app.route('/api/v2/businesses/<id>', methods=['GET','PUT','DELETE'])
@token_required
def business(current_user, id):
	""" route allows user to get, update and delete a business """

	if request.method=='GET':
		''' allows user view a business '''

		business = Business.query.filter_by(id=id).first()
		if business:
			business_info=business.business_object()

			return jsonify({'Status':'Success',
			                'Business': business_info}), 200

		return jsonify({'Status':'Failed',
			            'Message':'No business found'}), 404


	elif request.method=='PUT':
		''' method only allows business owner to edit it '''

		data=request.get_json()

		valid_name=re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', data['new_name'])
		valid_category=re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', data['category'])
		valid_location=re.match('^[A-Za-z]+[A-Za-z0-9 ]+$', data['location'])

		if valid_name and valid_category and valid_location:

			business = Business.query.filter_by(id=id).first()
			if business:
				if business.user_id==current_user:
					business.business_name=data['new_name']
					business.category=data['category']
					business.location=data['location']
					db.session.commit()

					return jsonify({'Status':'Success',
						            'message': 'Business Updated successfully'}), 200

				return jsonify({'Status':'Failed',
					            'Message':'You are not permitted'}), 403

			return jsonify({'Status':'Failed',
				            'Message':'No business found'}), 404

		return jsonify({'Status':'Failed',
			            'Message':'Only characters and digits are expected!'}), 403

	else:
		# delete business

		business = Business.query.filter_by(id=id).first()

		if not business:

			return jsonify({'Status':'Failed',
			                'Message': 'No business found!'}), 404
		else:

			if business.user_id==current_user:
				db.session.delete(business)
				db.session.commit()

				return jsonify({'Status':'Success',
					            'Message':'Business deleted successfully'}), 200

			return jsonify({'Status': 'Failed',
				            'Message':'You are not permitted'}), 403

		

@app.route('/api/v2/businesses/<id>/reviews', methods=['POST','GET'])
@token_required
def reviews(current_user, id):
	""" route allows user review a a business """

	if request.method=='POST':
		''' Reviewing a business '''
		data = request.get_json()

		valid_review=re.match('^[A-Za-z]+[A-Za-z0-9 ]{,200}$',data['review'])

		#if the data passes our validity check
		if valid_review:

			business = Business.query.filter_by(id=id).first()

			if not business:

				return jsonify({'Status':'Failed',
				                'Message':'Business not registered here!'}), 404

			else:
				new_review = Review( review=data['review'],business_id=id)
				db.session.add(new_review)
				db.session.commit()
				return jsonify({'Status':'Success',
					            'Message':'Review has been successfully added!'}), 201

		return jsonify({'Status':'Failed',
			            'Message':'Only characters and not beyond 200 charaters!'}), 403


	else:
		''' Get request '''
		reviews = Review.query.filter_by(business_id=id).all()

		if not reviews:

			return jsonify({'Status':'Failed',
			                'Message':'No reviews found!'}), 404

		else:

			author = User.query.filter_by(id = current_user).first()
			business = Business.query.filter_by(id=id).first()

			review_list=[]
			for review in reviews:
				review_info={}
				review_info['review']=review.review
				review_info['business_name']=business.business_name
				review_info['reviewed_on']=review.reviewed_on
				review_info['review_author']=author.username

				review_list.append(review_info)

			return jsonify({'Status':'Success',
					        'Review': review_list}), 200





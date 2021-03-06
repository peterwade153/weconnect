import datetime
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy 


#create our sqlachemy object
db = SQLAlchemy()

class User(db.Model):
	""" user table """

	__tablename__= 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100))
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(150))
	created_on = db.Column(db.DateTime, default=datetime.datetime.now)

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = generate_password_hash(password, method='sha256')


	def __repr__(self):
		# represnts object instance of model whenever it is queried
		return "<User :{}>".format(self.name)

class Business(db.Model):
	"""Business table """

	__tablename__= 'businesses'
	id = db.Column(db.Integer, primary_key=True)
	business_name = db.Column(db.String(50), unique=True)
	category = db.Column(db.String(50))
	location = db.Column(db.String(50))
	created_on = db.Column(db.DateTime, default=datetime.datetime.now)
	modified_on = db.Column(db.DateTime, default=datetime.datetime.now, 
		                                onupdate=datetime.datetime.now)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	user = db.relationship('User', backref=db.backref('businesses', 
		                                              lazy='dynamic'))


	def __init__(self, business_name, category, location, user_id):
		self.business_name = business_name
		self.category = category
		self.location = location
		self.user_id = user_id

	def save(self):
		"""saves the business"""
		db.session.add(self)
		db.session.commit()

	def get_businesses():
		""" returns businesses """
		businesses = Business.query.all()
		return businesses

	def get_business(id):
		""" return bussiness by id """
		business = Business.query.filter_by(id=id).first()
		return business

	def business_object(self):
		""" retuns business """
		return{
		      'id': self.id,
		      'business_name':self.business_name,
		      'category':self.category,
		      'location':self.location,
		      'created_on':self.created_on,
		      'modified_on':self.modified_on,
			  'owner':self.user_id
		}

class Review(db.Model):
	"""business reviews table"""

	__tablename__= 'reviews'
	id = db.Column(db.Integer, primary_key=True)
	review = db.Column(db.String(200))
	business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'))
	business = db.relationship('Business', backref=db.backref('reviews',
	                                                  lazy='dynamic'))
	reviewed_on = db.Column(db.DateTime, default=datetime.datetime.now)


	def __init__(self, review, business_id):
		self.review = review
		self.business_id = business_id

	def save(self):
		"""save the reviews"""
		db.session.add(self)
		db.session.commit()



class ExpiredToken(db.Model):
	""" model for blacklisted tokens"""

	__tablename__= 'expired_tokens'
	id = db.Column(db.Integer, primary_key=True)
	token = db.Column(db.String(200), unique=True, nullable=False)
	expired_on = db.Column(db.DateTime)

	def __init__(self, token):
		self.token = token
		self.expired_on = datetime.datetime.now()
		
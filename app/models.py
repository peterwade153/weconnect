from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
import app


#instantiate the db object with sqlalchemy
db = SQLAlchemy()

class User(db.Model):
	"""user table"""
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(100), unique = True)
	email = db.Column(db.String(100), unique = True)
	password = db.Column(db.String(150))

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = generate_password_hash(password, method='sha256')


	def __repr__(self):
		""" represents object instance of model whenever its queried"""
		return "<User :{}>.format(self.username)"


class Business(db.Model):
	"""business table"""
	__tablename__ = 'businesses'
	id = db.Column(db.Integer, primary_key = True)
	business_name = db.Column(db.String(100))
	business_category = db.Column(db.String(200))
	business_location = db.Column(db.String(100))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	user = db.relationship('User', backref = db.backref('businesses', lazy = 'dynamic'))

	def __init__(self, business_name, business_category, business_location, user_id):
		self.business_name = business_name
		self.business_category = business_category
		self.business_location = business_location
		self.user_id = user_id

	def save(self):
		"""saves the business"""
		db.session.add(self)
		db.session.commit()


class Review(db.Model):
	"""business reviews"""
	__tablename__ = 'reviews'
	id = db.Column(db.Integer, primary_key = True)
	review = db.Column(db.String(200))
	business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'))
	business = db.relationship('Business', backref = db.backref('reviews', lazy = 'dynamic'))

	def __init__(self, review, business_id):
		self.review = review
		self.business_id = business_id

	def save(self):
		"""save the reviews"""
		db.session.add(self)
		db.session.commit()

		
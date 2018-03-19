from flask_sqlalchemy import SQLAchemy 


#instantiate db object with sqlachemy
db = SQLAchemy()

class User(db.Model):
	""" user table """

	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(100), unique = True)
	email = db.Column(db.String(100), unique = True)
	password = db.Column(db.String(150))

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = generate_password_hash(password, method='sha256')

	def save(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def __repr__(self):
		# represnts object instance of model whenever it is queried
		return "<User :{}>".format(self.name)

class Business(db.Model):
	"""Business table """

	__tablename__ = 'businesses'
	id = db.Column(db.Integer, primary_key = True)
	business_name = db.Column(db.String(100))
	business_category = db.Column(db.String(200))
	business_location = db.Column(db.String(100))
	created_on = db.Column(db.Datetime, default = datetime.datetime.utcnow())
	modified_on = db.Column(db.Datetime, default = datetime.datetime.utcnow(), onupdate = datetime.datetime.utcnow())
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
		
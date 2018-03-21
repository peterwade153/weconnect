import os
from app import app
from app.models import db
from app.auth.views import auth


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db.init_app(app) #connecting sqlalchemy object to the app




@app.route('/api/v2/auth/logout' , methods = ['POST'])
def logout_user(self):
	""" route logs out a user """
###From Corey Schafer's CRUD App video on Youtube

from datetime import datetime
from app import mongo, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(mongo.db.Model, UserMixin):
    #id = mongo.db.Column(mongo.db.Integer, primary_key=True)
    Users = mongo.db.users(mongo.db.String(20), unique=True, nullable=False)
    #email = mongo.db.Column(mongo.db.String(120), unique=True, nullable=False)    
    password = mongo.Column(mongo.db.String(60), nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

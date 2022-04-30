import os
import random
import string

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

cwd = os.getcwd()

letters = string.ascii_letters
random_key = ''.join(random.choice(letters) for i in range(20))

app = Flask(__name__)

app.config['SECRET_KEY'] = random_key
app.config['DEBUG'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = f'{app.root_path}/uploads'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = ""
login_manager.init_app(app)

from app import models  
db.create_all()

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

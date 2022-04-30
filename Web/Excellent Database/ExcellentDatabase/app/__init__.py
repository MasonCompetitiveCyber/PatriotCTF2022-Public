import random
import string

from flask_session import Session
from flask import Flask

app = Flask(__name__)

letters = string.ascii_letters
random_key = ''.join(random.choice(letters) for i in range(20))
app.config['SECRET_KEY'] = random_key
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

USERNAMES = "A"
PASSWORDS = "B"

Session(app)
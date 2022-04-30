import random
import string

from flask import Flask

app = Flask(__name__)

letters = string.ascii_letters
random_key = ''.join(random.choice(letters) for i in range(20))
app.config['SECRET_KEY'] = random_key
app.config["SESSION_PERMANENT"] = False

confidential_settings = "|is_admin:0"

def admin(cookie):
    print("Chr = ", chr(cookie[-1]))
    if chr(cookie[-1]) == "1":
        return True
    else:
        return False
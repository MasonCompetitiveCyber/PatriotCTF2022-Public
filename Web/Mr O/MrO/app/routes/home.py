from ssl import ALERT_DESCRIPTION_DECOMPRESSION_FAILURE
from app import app
from app.models import User
from flask import render_template, render_template_string
from flask_login import current_user, login_required


@app.route('/')
@login_required
def home():
    usernames = []
    users = User.query.all()
    for user in users:
        usernames.append(user.username)
        
    return render_template('index.html', name=current_user.username, usernames=usernames)
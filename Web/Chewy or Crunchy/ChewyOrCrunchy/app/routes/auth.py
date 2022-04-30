from flask_login.utils import login_required
from app import app, db
from app.models import User
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    elif request.method=='POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if not username.isalnum():
            flash('Only alphanumeric characters are allowed in the username.', 'danger')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('home'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='GET':
        return render_template('signup.html')
    elif request.method=='POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if username == '' or password == '':
            flash('Username or password cannot be empty.', 'danger')
            return redirect(url_for('signup'))
        elif not username.isalnum():
            flash('Only alphanumeric characters are allowed in the username.', 'danger')
            return redirect(url_for('signup'))
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('signup'))
        
        new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        flash('Successfully created a new user! You can log in now.', 'success')
        return redirect(url_for('login'))
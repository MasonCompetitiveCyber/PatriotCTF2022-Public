import os

from app import app
from app.models import User
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename


@app.route('/admin', methods=['GET'])
@login_required
def admin():
    if current_user.admin:
        return render_template('admin.html', name=current_user.username)
    else:
        return redirect(url_for('home'))
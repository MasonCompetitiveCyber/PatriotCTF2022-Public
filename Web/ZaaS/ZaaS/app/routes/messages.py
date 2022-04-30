from app import app, db
from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from app.models import Message


@app.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    if request.method == 'GET':
        messages = Message.query.filter_by(msg_to=current_user.username).all()
        return render_template('messages.html', name=current_user.username, messages=messages)
    else:
        print(request.form)
        if "username" in request.form:
            msg_to = request.form.get("username")
            message = request.form.get("message")
            msg_from = current_user.username

            if message == '':
                flash('Don\'t leave the message empty.', 'danger')
                return redirect(url_for('home'))
            # elif "." in message or ">" in message or "{" in message or "}" in message:
            #     flash('Hey. No funny business. These characters are not allowed: .>{}', 'danger')
            #     return redirect(url_for('home'))
            if msg_to == 'Send to:':
                flash('Please select a person to send your message to.', 'danger')
                return redirect(url_for('home'))               

            msg = Message(msg_to=msg_to, msg_from=msg_from, message=message)
            db.session.add(msg)
            db.session.commit()

            flash('Your message has been sent!', 'success')
            return redirect(url_for('home'))

        else:
            Message.query.filter_by(msg_to=current_user.username).delete()
            db.session.commit()
            flash('Your messages have been cleared!', 'success')
            return redirect(url_for('home'))
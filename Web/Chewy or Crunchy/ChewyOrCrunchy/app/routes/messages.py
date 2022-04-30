from app import app, db
from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from app.models import Message
from app.bot import xssbot
import threading


@app.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    if request.method == 'GET':
        messages = Message.query.filter_by(msg_to=current_user.username).all()
        return render_template('messages.html', name=current_user.username, messages=messages)
    else: # POST
        print(request.form)
        if "username" in request.form: # a message was sent
            msg_to = request.form.get("username")
            message = request.form.get("message")
            msg_from = current_user.username

            if message == '':
                flash('Don\'t leave the message empty.', 'danger')
                return redirect(url_for('home'))
            elif "." in message or ">" in message or "{" in message or "}" in message:
                flash('Hey. No funny business. These characters are not allowed: .>{}', 'danger')
                return redirect(url_for('home'))
            if msg_to == 'Send to:':
                flash('Please select a person to send your message to.', 'danger')
                return redirect(url_for('home'))               

            msg = Message(msg_to=msg_to, msg_from=msg_from, message=message)
            db.session.add(msg)
            db.session.commit()

            # if msg sent to admin, run xssbot
            if msg_to == "admin":
                try:
                    t1 = threading.Thread(target=xssbot.run)
                    t1.start()
                except:
                    flash('admin failed to read message, please try again', 'warning')
                    return redirect(url_for('home'))   
                else:
                    flash('Your message has been sent! Admin will read it shortly.', 'success')
                    return redirect(url_for('home'))   
            else:
                flash('Your message has been sent!', 'success')

            return redirect(url_for('home'))
        else: # "clear messages" was pressed
            Message.query.delete()
            db.session.commit()
            flash('Everyone\'s messages have been cleared!', 'success')
            return redirect(url_for('home'))
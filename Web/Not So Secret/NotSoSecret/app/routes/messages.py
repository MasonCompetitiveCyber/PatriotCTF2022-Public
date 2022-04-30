from app import app, db
from flask import redirect, render_template, render_template_string, request, url_for, flash
from flask_login import current_user, login_required
from app.models import Message, User


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
            elif "." in message or "_" in message or "[" in message or "]" in message or "|" in message or "\\" in message or "<" in message or ">" in message or ";" in message:
                flash('Hey. No funny business. These characters are not allowed: ._[]|\\<>;', 'danger')
                return redirect(url_for('home'))
            if msg_to == 'Send to:':
                flash('Please select a person to send your message to.', 'danger')
                return redirect(url_for('home'))               

            msg = Message(msg_to=msg_to, msg_from=msg_from, message=message)
            db.session.add(msg)
            db.session.commit()

            # flash('Your message has been sent!', 'success')
            # return redirect(url_for('home'))
            return ssti_index_template(message)

        else:
            Message.query.filter_by(msg_to=current_user.username).delete()
            db.session.commit()
            flash('Your messages have been cleared!', 'success')
            return redirect(url_for('home'))

def ssti_index_template(msg):
    usernames = []
    users = User.query.all()
    for user in users:
        usernames.append(user.username)

    template = '''
    {% extends "nav_base.html" %}

    {% block below_nav %}

    <div class="px-4 py-5 text-center">
        <h1>Send Anybody A Message!</h1>
    </div>

    <div class="d-flex justify-content-center flex-column col-12">
        <div class="alert alert-success text-wrap align-self-center col-3 alert-dismissible" role="alert">
            <p style="color: black; margin-bottom: -5px;">Just sent your message: ''' + msg + '''</p>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    </div>

    <div class="container-fluid flex-column d-flex justify-content-center col-3">
        <!-- <form style='margin-left: -12px; margin-right: -12px' id='form' method='POST' name="msgForm"
            onsubmit="return validateMsg()" action='messages'> -->
        <form style='margin-left: -12px; margin-right: -12px' id='form' method='POST' name="msgForm" action='messages'>    
            <blockquote>
                <!-- <div class="alert alert-danger text-wrap align-self-center alert-dismissible" id="invalidChars"
                    aria-hidden="true" role="alert">
                    Hey. No funny business. These characters are not allowed:<br>
                    <p style="color: black; margin-bottom: -5px;">.>{}</p>
                </div> -->
                <div class='border blue align-self-center' style="height: 150px;">
                    <textarea id="msgBox" class='cursor border' type='text' name='message' placeholder='&block;'></textarea>
                </div>
            </blockquote>
            <select class="form-select bg-dark text-white" style="margin-top: -18px;" name="username" required>
                <option selected>Send to:</option>
                {% for username in usernames %}
                <option value={{username}}>To: {{username}}</option>
                {% endfor %}
            </select>
            <button class="btn border blue text-white wrapper mt-3" type="submit" id="sendMsg">Submit</button>
        </form>
    </div>

    {% endblock %}
    '''
    
    return render_template_string(template, name=current_user.username, usernames=usernames)
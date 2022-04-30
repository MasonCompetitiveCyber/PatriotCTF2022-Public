from app import app
from app.routes import home, auth, admin, messages, upload
from app.models import User
from app import db
from werkzeug.security import generate_password_hash

if __name__ == '__main__':
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", password="sha256$6QwIhZ2mB3crtuPD$707c80c2b886e64f2d8e98322e2768b1f5062495caa8449f6bb6bcd262158552", admin=True)
        db.session.add(admin)
        db.session.commit()

    app.run(debug=False, host='0.0.0.0', threaded=True, use_evalex=False)

from app import app
from app.routes import home, auth, admin, messages
from app.models import User
from app import db
from werkzeug.security import generate_password_hash

if __name__ == '__main__':
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", password="sha256$ZzRaNMjKKup1CN0f$40ba00964e7b48c345e4fbf10f38d246c5940b46d4d70a891312490f265234a7", admin=True)
        db.session.add(admin)
        db.session.commit()

    app.run(debug=False, host='0.0.0.0', threaded=True)

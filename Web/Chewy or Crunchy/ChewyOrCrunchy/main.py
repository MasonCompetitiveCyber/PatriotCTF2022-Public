from app import app
from app.routes import home, auth, messages, admin
from app.models import User
from app import db
from werkzeug.security import generate_password_hash

if __name__ == '__main__':
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", password="sha256$1lcx5Ru0$e25e68ce5a8876b171b785c7cd942fa51b5dd5de5be633a25735ef8b9116840d", admin=True)
        db.session.add(admin)
        db.session.commit()
    
    app.run(debug=False, host='0.0.0.0', threaded=True)

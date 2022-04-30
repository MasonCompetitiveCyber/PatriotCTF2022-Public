from app import app
from app.routes import home, auth, admin, messages, upload
from app.models import User
from app import db
from werkzeug.security import generate_password_hash

if __name__ == '__main__':
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", password="sha256$cG0gABB9nieWr4g2$97cee77447b0e5c0f76c2add88eca9291f3442e273dd22bd1d421365efd4fd52", admin=True)
        db.session.add(admin)
        db.session.commit()

    app.run(debug=True, host='0.0.0.0', threaded=True, use_evalex=False)

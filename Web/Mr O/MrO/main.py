from app import app
from app.routes import home, auth, admin, messages
from app.models import User
from app import db
from werkzeug.security import generate_password_hash

if __name__ == '__main__':
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", password="sha256$ldzahOmhc5UOQszA$1013deac316b2dc72f98b9a0508ff5a9c568b64abde259b3460353a47823f32b", admin=True)
        db.session.add(admin)
        db.session.commit()

    app.run(debug=False, host='0.0.0.0', threaded=True)

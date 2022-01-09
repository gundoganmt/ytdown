from ytdown import create_app, db
from ytdown.models import Video, Resolutions, Admin
from werkzeug.security import generate_password_hash

app = create_app()

@app.before_first_request
def populateDb():
    admin = db.session.query(Admin).first()
    if not admin:
        admin = Admin(username='admin', email="admin@gmail.com", full_name="John Doe",
            password=generate_password_hash("123456", method='sha256', salt_length=7))
        db.session.add(admin)
        db.session.commit()
    return True

if __name__ == '__main__':
    app.run(debug=True)

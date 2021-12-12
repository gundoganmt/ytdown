from flask_login import UserMixin
from ytdown import db

class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True, default="")
    surname = db.Column(db.String(50), nullable=True, default="")
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80))

    def get_full_name(self):
        return self.name + " " + self.surname

    def __repr__(self):
        return self.name + " " + self.surname

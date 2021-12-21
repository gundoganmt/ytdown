from flask_login import UserMixin
from ytdown import db

class Admin(UserMixin, db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=True, default="")
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return self.username

class Video(db.Model):
    __tablename__ = 'Video'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50))
    web_url = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.Text, nullable=True)
    download_date = db.Column(db.DateTime)
    res = db.relationship('Resolutions', backref='res', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return self.web_url

class Resolutions(db.Model):
    __tablename__ = 'Resolutions'
    id = db.Column(db.Integer, primary_key=True)
    download_url = db.Column(db.Text, nullable=False)
    token = db.Column(db.String(100), nullable=False)
    vid_id = db.Column(db.Integer, db.ForeignKey('Video.id'), nullable=False)

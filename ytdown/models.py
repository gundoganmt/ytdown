from flask_login import UserMixin
from ytdown import db

class Admin(UserMixin, db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=True, default="")
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(120), default='profile.png')

    def __repr__(self):
        return self.username

class Video(db.Model):
    __tablename__ = 'Video'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    source = db.Column(db.String(50))
    web_url = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.Text, nullable=True)
    dw_date = db.Column(db.String(50))
    res = db.relationship('Resolutions', backref='res', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return self.web_url

class Resolutions(db.Model):
    __tablename__ = 'Resolutions'
    id = db.Column(db.Integer, primary_key=True)
    download_url = db.Column(db.Text, nullable=False)
    token = db.Column(db.String(100), nullable=False)
    ext = db.Column(db.String(10))
    vid_id = db.Column(db.Integer, db.ForeignKey('Video.id'), nullable=False)

class Faq(db.Model):
    __tablename__ = 'Faq'
    id = db.Column(db.Integer, primary_key=True)
    faq_q = db.Column(db.String(250))
    faq_ans = db.Column(db.Text)

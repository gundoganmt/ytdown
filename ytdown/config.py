import psycopg2, os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '7c6b7967-dcba-4796-a261-f36b028144e3'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'ytdown.db') #"postgresql+psycopg2://postgres:WulIgtM5zk@localhost/commento"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = "smtp.zoho.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "support@pshort.net"
    MAIL_PASSWORD = "2U8IJi6qI4H2"

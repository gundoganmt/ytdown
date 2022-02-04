import psycopg2, os

class Config:
    SECRET_KEY = '7c6b7967-dcba-4796-a261-f36b028144e3' # random secret key
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    

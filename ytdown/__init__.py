from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from ytdown.config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'account.login'
login_manager.login_message = "Please login to see this page"

@login_manager.user_loader
def load_user(id):
    return Admin.query.get(int(id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    migrate = Migrate()

    db.init_app(app)
    csrf.init_app(app)
    with app.app_context():
        migrate.init_app(app,db)
        db.create_all()
    login_manager.init_app(app)

    from ytdown.account.views import account
    from ytdown.public.views import public
    app.register_blueprint(account)
    app.register_blueprint(public)

    return app

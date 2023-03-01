from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_USER = "SECRET USER"
DB_PASS = "SECRET"
DB_HOST = "mysql.agh.edu.pl"
DB_NAME = "SECRET NAME"
DB_PORT = 3306


def create_app():
    print(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}')
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRET KEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

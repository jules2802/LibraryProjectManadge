from os import path

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Manadge project'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from website.views.interface import v1
    from website.views.authentification import v1
    app.register_blueprint(v1)

    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = 'interface.home_page'
    login_manager.init_app(app)

    from website.models.user import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))#get is searching directly on the primarly key

    return app


def create_db(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Database created')
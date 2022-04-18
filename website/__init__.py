from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


from os import path

db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Secret Code'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .models import User, Profile, Link

    from .views import views
    from .auth import auth
    # from .admin import admin


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    # app.register_blueprint(admin, url_prefix='/')


    from .models import Link, User, Profile


    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # where flask reedirects us if the user is not logged in
    login_manager.init_app(app) # telling login manager which app we are using
     
    admin = Admin()
    admin.add_view(ModelView(User, db.session))
    admin.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # telling flask how we load a user

   
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")


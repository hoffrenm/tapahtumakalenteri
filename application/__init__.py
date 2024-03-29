from flask import Flask, url_for, redirect
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from os import urandom

app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

from application.auth import models 
from application.comments import models
from application.events import models

from application.auth.models import User, Role
from application.auth.forms import LoginForm

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from application import views
from application.auth import views
from application.events import views
from application.comments import views

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.login_manager.unauthorized_handler
def unauth_handler():
    return redirect(url_for('auth_login'))

try:
    db.create_all()
except:
    pass

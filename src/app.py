from os import environ 
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-squirrel'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///myDB.db' or 'sqlite:///building_codes.db'

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

from routes import *
from models import *
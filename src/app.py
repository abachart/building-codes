import os
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

uri = os.getenv("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-squirrel'
app.config['SQLALCHEMY_DATABASE_URI'] = uri or 'sqlite:///building_codes.db'

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

from routes import *
from models import *

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
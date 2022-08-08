from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-squirrel'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///building_codes.db'

db = SQLAlchemy(app)

# home page
@app.route('/')
@app.route('/index')
def home():
    return render_template('home.html')

from routes import *

# app name 
@app.errorhandler(404) 
def not_found(e): 
  return render_template('404.html')


if __name__ == '__main__':
    app.run()
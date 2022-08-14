from enum import unique
from src.app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128), unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    user_projects = db.relationship('UserProjects', backref='user', lazy='dynamic')
    user_locations = db.relationship('UserLocations', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'{self.username}'
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 

class UserProjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    
class UserLocations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    codes = db.relationship('ProjectCodes', backref='project', lazy='dynamic')
    
    def __repr__(self):
        return f'{self.name}'
    
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(64))
    city = db.Column(db.String(64))
    codes = db.relationship('LocationCodes', backref='location', lazy='dynamic')

    def __repr__(self):
        return f'{self.city}, {self.state}'

class ProjectCodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    code_id = db.Column(db.Integer, db.ForeignKey('code.id'))
     
    def __repr__(self):
        return f'{Code.query.get(self.code_id).name}, {Code.query.get(self.code_id).year}'
    
class LocationCodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    code_id = db.Column(db.Integer, db.ForeignKey('code.id'))
    
    def __repr__(self):
        return f'{Code.query.get(self.code_id).name}, {Code.query.get(self.code_id).year}'
    
class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    year = db.Column(db.Integer)
    link = db.Column(db.String(128))
    
    def __repr__(self):
        return f'{self.name}, {self.year}'
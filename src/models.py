from app import app, db

class BuildingCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    year = db.Column(db.Integer, unique=False)
    link = db.Column(db.String(150), unique=False)

    def __repr__(self):
        return f'{self.name}'
    
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_id = db.Column(db.Integer, db.ForeignKey('building_code.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

    def __repr__(self):
        return f'{BuildingCode.query.get(self.code_id).name}, {BuildingCode.query.get(self.code_id).year}'

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(40), unique=False)
    city = db.Column(db.String(40), unique=False)
    codes = db.relationship('Item', backref='location', lazy='dynamic')
    # state will also have federal option

    def __repr__(self):
        return f'{self.city}, {self.state}'
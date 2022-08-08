from app import db
from models import BuildingCode, Item, Location

l1 = Location(id=1, state='WA', city='City 1')
l2 = Location(id=2, state='WA', city='City 2')

c1 = BuildingCode(id=1, name='WA State Fire Code', year=2018, link='https://up.codes/viewer/washington/wa-fire-code-2018')
c2 = BuildingCode(id=2, name='NFPA 54 National Fuel Gas Code', year=2018, link='https://ahmad-tomasz.weebly.com/uploads/9/6/0/5/96054774/nfpa_54_ansi_z223.1.pdf')

db.session.add(l1)
db.session.add(l2)
db.session.add(c1)
db.session.add(c2)


db.session.commit()
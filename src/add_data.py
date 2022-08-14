from app import db
from models import User, UserProjects, UserLocations, Project, Location, ProjectCodes, LocationCodes, Code

u1 = User(id=1, username='user1')
u1.set_password('password')
u2 = User(id=2, username='user2')
u2.set_password('password')

l1 = Location(id=1, state='WA', city='City 1')
l2 = Location(id=2, state='WA', city='City 2')

p1 = Project(id=1, name='Project 1')
p2 = Project(id=2, name='Project 2')

c1 = Code(id=1, name='WA State Fire Code', year=2018, link='https://up.codes/viewer/washington/wa-fire-code-2018')
c2 = Code(id=2, name='NFPA 54 National Fuel Gas Code', year=2018, link='https://ahmad-tomasz.weebly.com/uploads/9/6/0/5/96054774/nfpa_54_ansi_z223.1.pdf')

db.session.add(u1)
db.session.add(u2)
db.session.add(l1)
db.session.add(l2)
db.session.add(p1)
db.session.add(p2)
db.session.add(c1)
db.session.add(c2)

db.session.commit()
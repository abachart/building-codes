import os
os.remove("D:\\vscode\projects\\building-codes\src2\\building_codes.db")
from app import db
from models import *
db.create_all()
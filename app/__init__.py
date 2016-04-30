from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

from models import *

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dev:dev@localhost/wishlist'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nbtgpccughvyvg:B-Nfv9o5llQAyv_crasERkAYcB@ec2-174-129-18-170.compute-1.amazonaws.com:5432/d1jv4v3ejj80l4'

#db.drop_all()
db.create_all()

db.session.commit() 

from . import views, models
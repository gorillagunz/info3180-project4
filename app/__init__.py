from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

from models import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dev:dev@localhost/wishlist'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ihztujtsyworlv:PamYRUGMSJkBmHAyVFXLadvhrd@ec2-107-21-229-87.compute-1.amazonaws.com:5432/d5u75njlgmd9q9'db.drop_all()
db.create_all()

db.session.commit() 

from app import views, models
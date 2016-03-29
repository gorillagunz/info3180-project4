import os
from app import app
from app import db
from flask import render_template, request, redirect, url_for, jsonify, Response
from .forms import WishlistForm
import time
from app.models import Profile, Wishlist, Item

app.secret_key ="REST SECRET"

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template("index.html")
    
@app.route('/wishlist/new', methods = ['GET', 'POST'])
def new_wishlist():
    form = WishlistForm()
    if request.method == 'POST' and form.validate_on_submit():
        print form.is_private.data
    return render_template("add_wishlist.html", form=form)

@app.route('/wishlist/', methods = ['GET', 'POST'])
def wishlist():
    return render_template("wishlist.html")


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
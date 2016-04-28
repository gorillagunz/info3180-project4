import os
from app import app
from app import db
from flask import render_template, request, redirect, url_for, jsonify, Response
from .forms import WishlistForm,ItemForm, LoginForm
import time
from app.models import Profile, Wishlist, Item
import requests
import BeautifulSoup
import urlparse
import validators

app.secret_key ="REST SECRET"

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template("login.html", form = form)
    else:
        em = form.email.data
        password = form.password.data
        
        user = db.session.query(Profile).filter_by(email=em, password=password).first()
        if user != None:
            return redirect(url_for("wishlists", userid = user.id))
        return render_template("login.html", form = form)

@app.route('/', methods = ['GET', 'POST'])
def home_login():
    # user = Profile(name="n", email="admin", password="pass")
    # db.session.add(user)
    # db.session.commit()
    return redirect(url_for('login'))

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template("index.html")
    
@app.route('/wishlist/new', methods = ['GET', 'POST'])
def new_wishlist():
    form = WishlistForm()
    if request.method == 'POST' and form.validate_on_submit():
        print form.is_private.data
    return render_template("add_wishlist.html", form=form)

@app.route('/user/<int:userid>/wishlists/', methods = ['GET', 'POST'])
def wishlists(userid):
    wishlists = db.session.query(Wishlist).filter_by(userid=userid)
    form = WishlistForm()
    return render_template("wishlists.html", wishlists=wishlists, form=form)

@app.route('/wishlist/<wishlist_id>', methods = ['GET', 'POST'])
def wishlist(wishlist_id):
    return render_template("wishlist.html", wishlist_id=wishlist_id)


@app.route('/wishlist/<wishlist_id>/new', methods = ['GET', 'POST'])
def new_item(wishlist_id):
    form = ItemForm()
    
    return render_template("add_item.html", form=form)

"""
    API SYSTEM
"""
@app.route('/api/user/register', methods=['POST'])
def api_register():
    name = request.data.get('name','')
    email = request.data.get('email', '')
    password = request.data.get('password','')
    user = db.session.query('Profile').filter(email=email)
    if user != []:
        return jsonify({"error":"1","data":{},'message':'not signed up'})

    else:
        user = Profile(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        response = jsonify({"error":"null","data":{'name':user.name,'email':user.email, 'user_id':user.id},"message":"Sucess"})

        return response
    return jsonify(user)

@app.route('/api/user/:id/wishlist', methods=['GET', 'POST'])
def api_wishlist(id):
    if request.method == 'GET':
        return 'GET'
    else:
        return 'POST'

@app.route('/api/thumbnail/process', methods=['GET'])
def api_thumbnail():
    url = request.args.get('url','')
    if url == "" or not validators.url(url):
        return jsonify({"error": "1","data": {},"message": "Unable to extract thumbnails"})
    else:
        data = {'thumbails':get_images(url)}
        return jsonify(error='Null',data=data, message="Success")

def get_images(url):
    images = []
    result = requests.get(url)
    soup = BeautifulSoup.BeautifulSoup(result.text)
    og_image = (soup.findAll('meta', property='og:image') or
                        soup.findAll('meta', attrs={'name': 'og:image'}))
    if og_image:
        for img in og_image:
            if validators.url(str(img['content'])):
                images += [img['content']]
    #print images 
    thumbnail_spec = soup.findAll('link', rel='image_src')
    if thumbnail_spec:
        for img in thumbnail_spec:
            if validators.url(str(img['href'])):
                images += [str(img['href'])]
    
    for img in soup.findAll("img", src=True):
        if "sprite" not in img["src"]:
            if validators.url(str(img['src'])):

                images += [str(img["src"])]
    return images


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
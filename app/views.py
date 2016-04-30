import os
from app import app
from app import db
from flask import render_template, request, redirect, url_for, jsonify, Response
from .forms import WishlistForm,ItemForm, LoginForm, SignUpForm
import time
from app.models import Profile, Wishlist, Item
import BeautifulSoup
import urlparse
import validators
from time import gmtime, strftime

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

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = SignUpForm()
    if request.method == 'GET':
        return render_template("signup.html", form = form)
    else:
        em = form.email.data
        password = form.password.data
        user = db.session.query(Profile).filter_by(email=em, password=password).first()
        if user != None:
            return redirect(url_for("wishlists", userid = user.id))
        name = form.name.data
        user1 = Profile(name, password, em)
        db.session.add(user1)
        db.session.commit()
        user2 = db.session.query(Profile).filter_by(email=em, password=password).first()

        if user2 != None:
            return redirect(url_for("wishlists", userid = user2.id))        
        return render_template("register.html", form = form)


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
    user = db.session.query(Profile).filter_by(id=userid).first()
    return render_template("wishlists.html", wishlists=wishlists, form=form, user=userid)

@app.route('/wishlist/<wishlist_id>', methods = ['GET', 'POST'])
def wishlist(wishlist_id):
    wishlist = db.session.query(Wishlist).filter_by(id=wishlist_id).first().title
    return render_template("wishlist.html", wishlist_id=wishlist_id, title=wishlist)


@app.route('/wishlist/<wishlist_id>/new', methods = ['GET', 'POST'])
def new_item(wishlist_id):
    form = ItemForm()
    if request.method == 'POST':
        wishlistid = wishlist_id
        user = db.session.query(Wishlist).filter_by(id=wishlist_id).first()
        userid = user.userid
        title = form.title.data
        desc=form.desc.data
        item_url = form.url.data
        image_url = form.img.data
        added_on = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        item = Item( userid, wishlistid, title, desc, image_url, item_url, added_on)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('wishlist',wishlist_id=wishlist_id))
    return render_template("add_item.html", form=form, wishlist_id=wishlist_id)

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

@app.route('/api/wishlist/new', methods=['GET','POST'])
def api_new_wishlist():
    user = request.args.get('userid','')
    title = request.args.get('title','')
    desc = request.args.get('desc', '')
    private = request.args.get('private', '')
    created_on = request.args.get('created_on', '')

    wishlist = Wishlist(user, title, desc, private, created_on )
    db.session.add(wishlist)
    db.session.commit()
    return jsonify(data=dict(wtitle=wishlist.title, w_id=wishlist.id))

@app.route('/api/user/<userid>/wishlists', methods=['GET','POST'])
def api_user_wishlists(userid):
    wishlists = db.session.query(Wishlist).filter_by(userid=userid)
    jwishlists = []
    for wishlist in wishlists:
        jwishlists.append(dict(wtitle=wishlist.title, w_id=wishlist.id))
    return jsonify(data=jwishlists)

@app.route('/api/user/<userid>/wishlist/<wishlistid>/items', methods=['GET','POST'])
def api_wishlist_items(userid, wishlistid):
    items = db.session.query(Item).filter_by(wishlistid=wishlistid)
    jitems = []
    for item in items:
        jitems.append(dict(title=item.title, url=item.item_url,desc=item.desc, img_url=item.image_url))
    return jsonify(data=jitems)
    
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
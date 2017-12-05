#!/usr/bin/python

from flask import Flask, render_template, \
    flash, request, redirect, url_for, jsonify, session
from flask_oauth import OAuth
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
import datetime
from functools import wraps
import json

# https://code.google.com/apis/console
GOOGLE_CLIENT_ID = 'YOUR-CLIENT-ID'
GOOGLE_CLIENT_SECRET = 'YOUR-CLIENT-SECRET'
REDIRECT_URI = '/oauth2callback'  # one of the Redirect URIs from Google APIs console

app = Flask(__name__)
app.secret_key = 'up to you to guest'
app.config['SESSION_TYPE'] = 'filesystem'
app.debug = True

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session = DBSession()

# Google authentication
oauth = OAuth()
google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)

"""
Ref to decorator: http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
"""


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('Login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def Index():
    categories = db_session.query(Category)
    items = db_session.query(Item).order_by(desc(Item.created_on)).limit(10)
    return render_template("index.html", categories=categories, items=items)


@app.route('/add-category', methods=['POST', 'GET'])
@login_required
def Add_Category():
    if request.method == 'GET':
        return render_template('add-category.html')
    elif request.method == 'POST':
        if request.form['title'] != '':
            category = Category(title=request.form['title'],
                                created_on=datetime.datetime.now())

            db_session.add(category)
            db_session.commit()

            flash('Category was successfully added', 'success')
            return redirect(url_for('Index'))
        else:
            return render_template('400.html')


@app.route('/items/<int:catID>')
def Items(catID):
    current_category = db_session.query(Category).get(catID)
    categories = db_session.query(Category)
    items = db_session.query(Item).filter_by(cid=catID)\
                      .order_by(desc(Item.created_on))
    return render_template('items.html',
                           current_category=current_category,
                           categories=categories, items=items)


@app.route('/item-details/<int:itemID>')
def Item_Details(itemID):
    item = db_session.query(Item).get(itemID)
    return render_template('item-details.html', item=item)


@app.route('/add-item', methods=['GET', 'POST'])
@login_required
def Add_Item():
    if request.method == 'GET':
        categories = db_session.query(Category)
        return render_template('add-item.html', categories=categories)
    elif request.method == 'POST':
        if request.form['title'] != '' and request.form['cid'] != '':
            item = Item(title=request.form['title'],
                        desc=request.form['desc'],
                        cid=request.form['cid'],
                        created_on=datetime.datetime.now())

            db_session.add(item)
            db_session.commit()

            flash('Item was successfully added', 'success')
            return redirect(url_for('Index'))
        else:
            return render_template('400.html')


@app.route('/edit-item/<int:itemID>', methods=['GET', 'POST'])
@login_required
def Edit_Item(itemID):
    item = db_session.query(Item).get(itemID)

    if request.method == 'GET':
        categories = db_session.query(Category)
        return render_template('edit-item.html',
                               item=item, categories=categories)
    elif request.method == 'POST':
        if request.form['title'] != '' and request.form['cid'] != '':
            item.title = request.form['title']
            item.desc = request.form['desc']
            item.cid = request.form['cid']

            db_session.commit()

            flash('Item was successfully updated', 'success')
            return redirect(url_for('Item_Details', itemID=item.id))
        else:
            return render_template('400.html')


@app.route('/delete-item/<int:itemID>', methods=['GET', 'POST'])
@login_required
def Delete_Item(itemID):
    if request.method == 'GET':
        return render_template('delete-item.html')
    elif request.method == 'POST':
        item = db_session.query(Item).get(itemID)

        if item is None:
            flash('Cannot delete the item as it is not existing!', 'danger')
            return redirect(url_for('Index'))
        else:
            db_session.delete(item)
            db_session.commit()

            flash('Item was deleted successfully!', 'success')
            return redirect(url_for('Index'))


@app.route('/login', methods=['GET', 'POST'])
def Login():
    if get_access_token() is None:
        callback=url_for('authorized', _external=True)
        return google.authorize(callback=callback)
    else:
        flash('You have been logged in already!', 'success')
        return redirect(url_for('Index'))

@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''

    access_token = session.get('access_token')[0]
    from urllib2 import Request, urlopen, URLError
 
    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)

        return redirect(url_for('Login'))
 
    # get json of user info
    user_info = json.loads(res.read())
    
    # store username in session
    session['username'] = user_info['email']

    user = db_session.query(User).filter_by(username=user_info['email']).first()
    
    # Create new user if he is not existed
    if user is None:
        user = User(username=user_info['email'],
                    password='')
    
        db_session.add(user)
        db_session.commit()

    flash('You has been logged in successfully!', 'success')
    return redirect(url_for('Index'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')


@app.route('/logout')
def Logout():
    session.pop('access_token', None)
    session.pop('username', None)
    return redirect(url_for('Index'))


@app.route('/catalog.json')
@login_required
def Catalog_JSON():
    categories = db_session.query(Category)

    return jsonify(Category=[i.serialize for i in categories])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

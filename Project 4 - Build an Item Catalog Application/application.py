from flask import Flask, render_template, flash, request, redirect, url_for, jsonify, session
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'up to you to guest'
app.config['SESSION_TYPE'] = 'filesystem'

"""
Ref to decorator: http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
"""
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'username' in session:
            return redirect(url_for('Login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
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
			category = Category(title=request.form['title'], created_on=datetime.datetime.now())
         
			db_session.add(category)
			db_session.commit()
         
			flash('Category was successfully added', 'success')
			return redirect(url_for('Index'))
		else:
			return render_template('400.html')

@app.route('/items/<int:catID>')
@login_required
def Items(catID):
	current_category = db_session.query(Category).get(catID)
	categories = db_session.query(Category)
	items = db_session.query(Item).filter_by(cid=catID).order_by(desc(Item.created_on))
	return render_template('items.html', current_category=current_category, categories=categories, items=items)

@app.route('/item-details/<int:itemID>')
@login_required
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
			item = Item(title=request.form['title'], desc=request.form['desc'], cid=request.form['cid'], created_on=datetime.datetime.now())
			
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
		return render_template('edit-item.html', item=item, categories=categories)
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
		
		if item == None:
			flash('Cannot delete the item as it is not existing!', 'danger')
			return redirect(url_for('Index'))
		else:
			db_session.delete(item)
			db_session.commit()
			
			flash('Item was deleted successfully!', 'success')
			return redirect(url_for('Index'))

@app.route('/login', methods=['GET', 'POST'])
def Login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if username is None or password is None:
			flash('Missing username or password', 'danger')
			return redirect(url_for('Login'))
		
		user = db_session.query(User).filter_by(username=username).first()
		if user.verify_password(password) is False:
			flash('Invalid username or password! Try again', 'danger')
			return redirect(url_for('Login'))
		else:
			session['username'] = username
			return redirect(url_for('Index'))

@app.route('/logout')
@login_required
def Logout():
	session.pop('username', None)
	return redirect(url_for('Login'))
	
@app.route('/register', methods=['GET', 'POST'])
def Register():
	if request.method == 'GET':
		return render_template('register.html')
	elif request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if username is None or password is None:
			flash('Missing username or password', 'danger')
			return redirect(url_for('Register'))
		
		user = db_session.query(User).filter_by(username=username).first()
		if user is not None:
			flash('Username has been registered, try another!', 'danger')
			return redirect(url_for('Register'))
		
		# Save new user
		user = User(username=username)
		user.hash_password(password)
		db_session.add(user)
		db_session.commit()
		flash('User was successfully added', 'success')
		return redirect(url_for('Login'))
			

@app.route('/catalog.json')
@login_required
def Catalog_JSON():
	categories = db_session.query(Category)
	
	return jsonify(Category=[i.serialize for i in categories])

if __name__ == '__main__':
    
	engine = create_engine('sqlite:///catalog.db')
	Base.metadata.bind = engine
	
	DBSession = sessionmaker(bind=engine)
	db_session = DBSession()

	app.debug = True
	app.run(host = '0.0.0.0', port = 8080)

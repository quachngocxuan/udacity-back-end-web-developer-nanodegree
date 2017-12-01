from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
import datetime


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
	
	
@app.route('/')
def Index():
	categories = session.query(Category)
	items = session.query(Item).order_by(desc(Item.created_on)).limit(10)
	return render_template("index.html", categories=categories, items=items)
	
@app.route('/add-category', methods=['POST', 'GET'])
def Add_Category():
	if request.method == 'GET':
		return render_template('add-category.html')
	elif request.method == 'POST':
		if request.form['title'] != '':
			category = Category(title=request.form['title'], created_on=datetime.datetime.now())
         
			session.add(category)
			session.commit()
         
			flash('Category was successfully added')
			return redirect(url_for('Index'))
		else:
			return render_template('400.html')

@app.route('/items/<int:catID>')
def Items(catID):
	current_category = session.query(Category).filter_by(id=catID).first()
	categories = session.query(Category)
	items = session.query(Item).filter_by(cid=catID).order_by(desc(Item.created_on))
	return render_template('items.html', current_category=current_category, categories=categories, items=items)

@app.route('/item-details/<int:itemID>')
def Item_Details(itemID):
	item = session.query(Item).filter_by(id=itemID).first()
	return render_template('item-details.html', item=item)

@app.route('/add-item', methods=['GET', 'POST'])
def Add_Item():
	if request.method == 'GET':
		categories = session.query(Category)
		return render_template('add-item.html', categories=categories)
	elif request.method == 'POST':
		if request.form['title'] != '' and request.form['cid'] != '':
			item = Item(title=request.form['title'], desc=request.form['desc'], cid=request.form['cid'], created_on=datetime.datetime.now())
			
			session.add(item)
			session.commit()
			
			flash('Item was successfully added')
			return redirect(url_for('Index'))
		else:
			return render_template('400.html')
			
@app.route('/edit-item/<int:itemID>', methods=['GET', 'POST'])
def Edit_Item(itemID):
	item = session.query(Item).get(itemID)
	
	if request.method == 'GET':
		categories = session.query(Category)
		return render_template('edit-item.html', item=item, categories=categories)
	elif request.method == 'POST':
		if request.form['title'] != '' and request.form['cid'] != '':
			item.title = request.form['title']
			item.desc = request.form['desc']
			item.cid = request.form['cid']
			
			session.commit()
			
			flash('Item was successfully updated')
			return redirect(url_for('Index'))
		else:
			return render_template('400.html')

@app.route('/delete-item', methods=['GET', 'POST'])
def Delete_Item():
	return render_template('delete-item.html')

@app.route('/login', methods=['GET', 'POST'])
def Login():
	return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def Register():
	return render_template('register.html')
	
if __name__ == '__main__':
    
	engine = create_engine('sqlite:///catalog.db')
	Base.metadata.bind = engine
	
	DBSession = sessionmaker(bind=engine)
	session = DBSession()

	app.debug = True
	app.run(host = '0.0.0.0', port = 8080)

from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
	
	
@app.route('/')
def Index():
	return render_template("index.html")

@app.route('/add-category', methods=['POST', 'GET'])
def Add_Category():
	if request.method == 'GET':
		if not request.form['title']:
			flash('Please enter all the fields', 'error')
		else:
			category = Category(title=request.form['title'])
         
			session.add(category)
			session.commit()
         
			flash('Category was successfully added')
			return redirect(url_for('Index'))
	
	return render_template('add-category.html')

@app.route('/items')
def Items():
	return render_template('items.html')

@app.route('/item-details')
def Item_Details():
	return render_template('item-details.html')

@app.route('/add-item', methods=['GET', 'POST'])
def Add_Item():
	categories = session.query(Category)
	return render_template('add-item.html', categories=categories)

@app.route('/edit-item', methods=['GET', 'POST'])
def Edit_Item():
	return render_template('edit-item.html')

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

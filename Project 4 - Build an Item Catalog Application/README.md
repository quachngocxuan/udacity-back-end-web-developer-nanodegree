# Udacity - Catalog Item Project

## Table of Contents

* [Project Overview](#project-overview)
* [How to Run](#how-to-run)
* [Features](#features)
* [Database](#database)
* [Credits](#credits)
* [References](#references)

## Project Overview
This project is an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## How to Run

### Installation required packages

1. Firstly, you need install ```Flask``` if any
```
$ pip install Flask
```

2. And then install ```SQLAlchemy``` to map objects with database
```
$ pip install flask-sqlalchemy
```

3. And then install the ```passlib```
```
$ sudo pip install passlib
```

### Configure the database
It may need to change writable permission for the db file
```
$ sudo chmod a+w catalog.db
```

### Setup Google Login
Create a Google credential from [this link](https://console.developers.google.com/apis/credentials).
And replace ```client-id``` and ```secret key``` in ```application.py```

### Running server
```
$ python application.py
```

### Open the application
This depends on your address of server. You should open a web browser and enter the address of server with the port 8080
```
http://<your-server-name-or-IP>:8080/
```

## Features
The application has some following features:

1. The homepage displays all current categories along with the latest added items.
![homepage](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/598e0c98_localhost8080/localhost8080.png "Homepage")

2. Selecting a specific category shows all the items available for that category.
![category details](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/598e0d0e_snowboarding/snowboarding.png "Category details")

3. Selecting a specific item shows you specific information of that item.
![item details](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/598e0d7a_item/item.png "Item details")

4. After logging in, a user has the ability to add, update, or delete item info.
![crud](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/598e0df0_edititem/edititem.png "CRUD")
![crud](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/598e0e51_snowboardloggedin/snowboardloggedin.png "CRUD")
![crud](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/598e0e8c_snowboardedit/snowboardedit.png "CRUD")
![crud](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/598e0ec8_snowboarddelete/snowboarddelete.png "CRUD")

5. The application provides a JSON endpoint, at the very least.
![catalog.json](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/598e0f11_catalogjson/catalogjson.png "Catalog JSON")

## Database

This application works on the database with three tables as below details:

Table "category"
```
 Column      |           Type           |                       Modifiers                       
-------------+--------------------------+-------------------------------------------------------
 title       | text                     | not null
 created_on  | datetime                 | not null
 id          | integer                  | not null primary_key
```
 
Table "item"
```
 Column      |  Type    |                      Modifiers                       
-------------+----------+------------------------------------------------------
 title       | text     | not null
 desc        | text     | 
 created_on  | datetime | not null
 cid         | text     | not null
 id          | integer  | not null primary_key
```   
    
Table "user"
```
 Column   |           Type           |                    Modifiers                     
----------+--------------------------+--------------------------------------------------
 username | text                     | not null primary_key
 password | text                     | 
```

## Credits
- [JQuery](https://jquery.com/) for frontend interaction
- [Bootstrap](https://getbootstrap.com/) for frontend interface
- Login form: thanks to [Simple login form](https://bootsnipp.com/snippets/featured/simple-login-form-bootsnipp-style-colorgraph)
- Form validation: thanks to [ParsleyJS](http://parsleyjs.org/)

## References
- [Login require Decorator](http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/)
- [Login to your Flask app with Google](https://pythonspot.com/en/login-to-flask-app-with-google/)

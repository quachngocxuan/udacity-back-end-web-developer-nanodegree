# My Neighbourhood Map Project

## Table of Contents

* [Project Overview](#project-overview)
* [How to Run](#how-to-run)
* [Features](#features)
* [Creadits](#credits)

## Project Overview


## How to Run

It may need to change writable permission for the db file
```
$ sudo chmod a+w catalog.db
```

## Features
The application has some following features:


## Tables

This tool works on the database with three tables as below details:

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
 user     | text                     | not null primary_key
 password | text                     | 
```

## Credits
- [JQuery](https://jquery.com/) for frontend interaction
- [Bootstrap](https://getbootstrap.com/) for frontend interface
- Login form: thanks to [Simple login form](https://bootsnipp.com/snippets/featured/simple-login-form-bootsnipp-style-colorgraph)
- Form validation: thanks to [ParsleyJS](http://parsleyjs.org/)
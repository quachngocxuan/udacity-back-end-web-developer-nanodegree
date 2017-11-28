# Logs Analysis Tool

## Table of Contents

* [Project Overview](#project-overview)
* [Package Requirement](#package-requirement)
* [How to Run](#how-to-run)
* [Tables](#tables)

## Project Overview

This project mines the news database to answer 3 questions.
1. List of most popular articles
2. List of most popular authors
3. List of days having error rate above 1%

## Package Requirement

In order to run this project, you should install this Python's package: ```pgdb```

Go to [this page](http://www.pygresql.org/contents/install.html) to be guided to install it.

## How to Run

From your command line, follows these instructions:

1. Import postgresql's database
If you don't execute inside predefined VM by Udacity, you have to import your own 'news' database from the file newsdata.sql by these commands:
```
sudo su
pip install psycopg2
sudo service postgresql start
sudo su - postgres
psql
CREATE ROLE fullstack WITH LOGIN PASSWORD 'fullstack';
CREATE DATABASE news;
GRANT ALL PRIVILEGES ON DATABASE news TO fullstack;
\q
cd Project\ 3\ -\ Logs\ Analysis/
psql -d news -f newsdata.sql
psql
\c news
GRANT ALL PRIVILEGES ON TABLE articles TO fullstack;
GRANT ALL PRIVILEGES ON TABLE authors TO fullstack;
GRANT ALL PRIVILEGES ON TABLE log TO fullstack;
\q
```

2. Change the postgresql account in the source file:
My default postgresql's account is 'fullstack', you should change this account that be suitable if you execute from udacity's VM

3. Go to the project folder containing this project's source:

 ```
cd this_project_source
```

4. Run the script to generate log discovering results

 ```
python logs_analysis.py
```

When you run this code with error, it may Python has not been installed yet. Please follow this tutorial to install Python: [Properly Installing Python](http://docs.python-guide.org/en/latest/starting/installation/)

## Tables

This tool works on the database with three tables as below details:

Table "public.articles"
```
 Column |           Type           |                       Modifiers                       
--------+--------------------------+-------------------------------------------------------
 author | integer                  | not null
 title  | text                     | not null
 slug   | text                     | not null
 lead   | text                     | 
 body   | text                     | 
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('articles_id_seq'::regclass)
```
 
Table "public.authors"
```
 Column |  Type   |                      Modifiers                       
--------+---------+------------------------------------------------------
 name   | text    | not null
 bio    | text    | 
 id     | integer | not null default nextval('authors_id_seq'::regclass)
```   
    
Table "public.log"
```
 Column |           Type           |                    Modifiers                     
--------+--------------------------+--------------------------------------------------
 path   | text                     | 
 ip     | inet                     | 
 method | text                     | 
 status | text                     | 
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('log_id_seq'::regclass)
```
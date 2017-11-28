1. To start postgresql
sudo su
sudo service postgresql start

2. Run psql to run commands
sudo su - postgres
psql

3. Quit psql (in psql)
\q and press enter

4. Create user
CREATE ROLE username WITH LOGIN PASSWORD 'quoted password' [OPTIONS];

5. List current users (in psql)
\du

6. Create new DB
CREATE DATABASE news;

7. Grant user privileges on DB
GRANT ALL PRIVILEGES ON DATABASE dbname TO username;

8. Grant user privileges on table
GRANT ALL PRIVILEGES ON TABLE tablename TO username;

9. List databases (in psql)
\list

10. Explore DB's tables
psql -d news

11. Explore a table (in psql)
\d table_name

12. Go into table (in psql)
\c table_name

--------------
CONSOLE LOGS

sudo su
pip install pygresql
sudo service postgresql start
sudo su - postgres
psql
CREATE ROLE fullstack WITH LOGIN PASSWORD 'fullstack';
CREATE DATABASE news;
GRANT ALL PRIVILEGES ON DATABASE news TO fullstack;
\q
cd /home/ubuntu/workspace/Udacity-Backend\ Nano\ Degree/Project\ 3\ -\ Logs\ Analysis/
wget https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
unzip newsdata
psql -d news -f newsdata.sql
psql
\c news
GRANT ALL PRIVILEGES ON TABLE articles TO fullstack;
GRANT ALL PRIVILEGES ON TABLE authors TO fullstack;
GRANT ALL PRIVILEGES ON TABLE log TO fullstack;
\q


-----------
News DB

Table "public.articles"

 Column |           Type           |                       Modifiers                       
--------+--------------------------+-------------------------------------------------------
 author | integer                  | not null
 title  | text                     | not null
 slug   | text                     | not null
 lead   | text                     | 
 body   | text                     | 
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('articles_id_seq'::regclass)
 
 
Table "public.authors"
 
 Column |  Type   |                      Modifiers                       
--------+---------+------------------------------------------------------
 name   | text    | not null
 bio    | text    | 
 id     | integer | not null default nextval('authors_id_seq'::regclass)
Indexes:
    "authors_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)
    
    
Table "public.log"

 Column |           Type           |                    Modifiers                     
--------+--------------------------+--------------------------------------------------
 path   | text                     | 
 ip     | inet                     | 
 method | text                     | 
 status | text                     | 
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('log_id_seq'::regclass)
Indexes:
    "log_pkey" PRIMARY KEY, btree (id)
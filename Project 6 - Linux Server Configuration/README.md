# Linux Server Configuration - Udacity Project

## Overview
This project, I created an Linux server instance on Linode.com

**Server information**
- The IP address: 172.104.178.228
- SSH port: 2200

**The complete URL to your hosted web application:** http://fix9999.com

**A summary of software you installed and configuration changes made.**
- pip-8.1.1
- psycopg2-2.7.3.2
- sqlalchemy-1.1.15
- postgresql-9.5
- postgresql-contrib
- git 2.7.4
- apache2
- libapache2-mod-wsgi
- Flask-0.12.2 Jinja2-2.10 MarkupSafe-1.0 Werkzeug-0.12.2 click-6.7 itsdangerous-0.24
- flask-sqlalchemy-2.3.2
- passlib-1.7.1
- flask_oauth

**Configuration changes:**
- Changes in the file /etc/ssh/sshd_config
* Port 2200
* PermitRootLogin without-password
* PasswordAuthentication no
- Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123).
- Change timezone to UTC

**A list of any third-party resources you made use of to complete this project:**
- [Changing the SSH Port for Your Linux Server](https://vn.godaddy.com/help/changing-the-ssh-port-for-your-linux-server-7306)
- [How To Setup a Firewall with UFW on an Ubuntu and Debian Cloud Server](https://www.digitalocean.com/community/tutorials/how-to-setup-a-firewall-with-ufw-on-an-ubuntu-and-debian-cloud-server)
- [How To Create a Sudo User on Ubuntu ](https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-ubuntu-quickstart)
- [How To Set Up SSH Keys](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys--2)
- [How do I change the timezone to UTC?](https://askubuntu.com/questions/117359/how-do-i-change-the-timezone-to-utc)
- [How To Install and Use PostgreSQL on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04)
- [SQLAlchemy quick start with PostgreSQL](https://suhas.org/sqlalchemy-tutorial/)
- [How To Set Up an Apache, MySQL, and Python (LAMP) Server Without Frameworks on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-apache-mysql-and-python-lamp-server-without-frameworks-on-ubuntu-14-04)
- [Login to your Flask app with Google](https://pythonspot.com/en/login-to-flask-app-with-google/)
- [AWS-LAPP-config](https://github.com/OscarDCorbalan/AWS-LAPP-config)

**Locate the SSH key you created for the grader user:**
The keys pair generated are place in the folder: /home/grader/.ssh/ with two files:
- id_rsa.pub : public key (need by server)
- id_rsa: private key (should be removed here and store on client)

## Installation guide

### Update all currently installed packages.
Run the command (on Ubuntu) to update packages
```
$ sudo apt-get update
$ sudo apt-get upgrade
```

### Change SSH port:
1. Connect to your server via SSH
2. Switch to the root user
```
$ sudo su
```
3. Run the following command:
```
$ vi /etc/ssh/sshd_config
```
4. Locate the following line:
```
# Port 22
```
5. Remove # and change 22 to 2200
6. Restart the sshd service by running the following command:
```
$ service sshd restart
```

### Setup a Firewall with UFW
To make sure UFW is installed, run the command
```
$ sudo apt-get install ufw
```

Check the status of UFW by typing
```
$ sudo ufw status
```
Right now, it will probably tell you it is inactive.

If your VPS is configured for IPv6, ensure that UFW is configured to support IPv6 so that will configure both your IPv4 and IPv6 firewall rules. To do this, open the UFW configuration with this command:
```
$ sudo vi /etc/default/ufw
```
Then make sure "IPV6" is set to "yes", like so:
```
IPV6=yes
```
Save and quit. Then restart the firewall with the following commands:
```
$ sudo ufw disable
$ sudo ufw enable
```

UFW’s defaults are to deny all incoming connections and allow all outgoing connections.
```
$ sudo ufw default deny incoming
$ sudo ufw default allow outgoing
```

Our SSH server is running on port 2222, we could enable connections with the following command
```
$ sudo ufw allow 2200/tcp
```
And deny default the SSH port 22
```
$ sudo ufw deny ssh
```

Allow HTTP
```
$ sudo ufw allow www
```

Allow NTP port 123
```
$ sudo ufw allow 123/udp
```

### Give grader access

Add grader user
```
$ adduser grader
```
and enter information for this user

Use the usermod command to add the user to the sudo group.
```
$ usermod -aG sudo grader
```

### Generate SSH key for grader
Generate key pair
```
$ ssh-keygen -t rsa
```

Place the public key on the virtual server
``` 
$ cat ~/.ssh/id_rsa.pub | ssh root@172.104.178.228 -p 2200 "mkdir -p ~/.ssh && cat >>  ~/.ssh/authorized_keys"
```
and press 'yes'

Disable the Password for Login
```
$ sudo vi /etc/ssh/sshd_config
```

Within that file, find the line that includes PermitRootLogin and modify it to ensure that users can only connect with their SSH key:
```
PermitRootLogin without-password
```

And change this configuration to 'no'
```
PasswordAuthentication no
```

Put the changes into effect:

```
$ service sshd restart
```

### Configure the local timezone to UTC.
Run the command 
```
$ sudo dpkg-reconfigure tzdata
```
and then choose 'None of above' and then choose 'UTC'

### Install and configure Apache to serve a Python mod_wsgi application.
Install pip
```
$ sudo apt install python-pip
```

Install SqlAlchemy
```
$ sudo pip install psycopg2 sqlalchemy
```

Install Flask oauth for Google login
```
$ sudo pip install flask_oauth
```

Install git
```
$ sudo apt-get install git
```

Install Apache2
```
$ sudo apt-get install apache2
```

Install Mod WSGI and enable it
```
$ sudo apt-get install python-setuptools libapache2-mod-wsgi
$ sudo a2enmod wsgi
```

Install Flask & flask-sqlalchemy
```
$ pip install Flask
$ pip install flask-sqlalchemy
```

Install passlib
```
$ pip install passlib
```

### Install and configure PostgreSQL
Install the Postgres package
```
$ sudo apt-get install postgresql postgresql-contrib
```
Switch over to the postgres account on your server by typing:
```
$ sudo -i -u postgres
```
Now access a Postgres prompt immediately by typing:
```
$ psql
```
Create database
```
CREATE DATABASE catalog;
```
Create user
```
CREATE USER uda WITH PASSWORD 'ppp';
```
ppp is the real password

Grant privileges access
```
GRANT ALL PRIVILEGES ON DATABASE catalog TO uda;
```

Update ```database_setup``` to migrate from sqlite to postgreSQL by change ```create_engine```. Change ```PASSWORD``` to your DB password.
```
create_engine('postgresql+psycopg2://uda:PASSWORD@localhost/catalog')
```
and then execute the command to setup database
```
$ python database_setup.py
```

### Create application folder

Clone project
```
$ git clone https://github.com/quachngocxuan/udacity-fullstack-web-developer-nanodegree.git
```

Create folder of web application in apache
```
$ mkdir /var/www/catalog
```

And go to the source folder and run the command to copy source to the web app folder
```
$ cp -r * /var/www/catalog
```

Create the WSGI file
```
$ cd /var/www/catalog
$ sudo vim catalog.wsgi
```
Type in the following lines of code
```
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog")
from application import app as application
```

We must register Python with Apache. To start, we disable multithreading processes.
```
$ sudo a2dismod mpm_event
```
Then, we give Apache explicit permission to run scripts.
```
$ sudo a2enmod mpm_prefork cgi
```

Next, we modify the actual Apache configuration, to explicitly declare Python files as runnable file and allow such executables. Open the configuration file using nano or your favorite text editor.
```
$ sudo nano /etc/apache2/sites-enabled/000-default.conf
```
change inside the tag <VirtualHost>:
```
        ServerName Your-Server-Name
        ServerAdmin Your-Eamil
        DocumentRoot /var/www/catalog
        WSGIScriptAlias / /var/www/catalog/catalog.wsgi
        <Directory /var/www/catalog/>
                Order allow,deny
                Allow from all
        </Directory>
```
then restart the apache server
```
$ sudo service apache2 restart
```

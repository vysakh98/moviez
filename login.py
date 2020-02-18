#!/usr/bin/python3 

import cgi
import cgitb
import hashlib, binascii, os
cgitb.enable()
from jinja2 import Template, Environment, FileSystemLoader

print("Content-Type: text/html")
print()
print("<br>")
# Create instance of FieldStorage
form_data = cgi.FieldStorage()

# Get data from fields
username = form_data["username"].value
password = form_data["password"].value

#print(username)
#print(password)


import pymysql
from pymysql.err import MySQLError
#password1 = form_data["pwd"].value
#salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
conn = pymysql.connect(
    db='pyb83',
    user='pyb83',
    passwd='qeAYUn4I',
    host='localhost')
#c = conn.cursor()
c =conn.cursor(pymysql.cursors.Cursor)


sql1='SELECT COUNT(*) FROM SIGNUP WHERE username="%s"'
c.execute(sql1 %username)
username_count=c.fetchone()
conn.commit()
sql2='SELECT COUNT(salt_value) FROM SIGNUP WHERE username="%s"'
c.execute(sql2 %username)
salt_count=c.fetchone()
conn.commit()
if username_count[0]!=0 and salt_count[0]!=0:
    login_sql = 'SELECT salt_value FROM SIGNUP WHERE username="%s"'
    c.execute(login_sql % username)
    row=c.fetchone()
    usersalt=row[0]
    conn.commit()
    sql='SELECT password FROM SIGNUP WHERE username="%s"'
    c.execute(sql % username)
    row1=c.fetchone()
    userpwd=row1[0]
    conn.commit()
    print(userpwd)
    def verify_password(stored_password,stored_salt,provided_password):
        
        salt = stored_salt
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',provided_password.encode('utf-8'),salt.encode('ascii'),100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        #print(pwdhash)
        return pwdhash == stored_password


    is_authenticated_user = verify_password(userpwd,usersalt,password) 


    if (is_authenticated_user):
        redirectURL = "http://pyb83.specind.net/home.html"
    else:
        redirectURL = "http://pyb83.specind.net/templates/login.html"
else:
    redirectURL="http://pyb83.specind.net/templates/login.html"
print("<html>")
print("<head>")
print('<meta http-equiv="refresh" content="0;url='+str(redirectURL)+'" />')
print("</head>")
print("</html>")
    
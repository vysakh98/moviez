#!/usr/bin/python3 

import cgi
import cgitb
import hashlib, binascii, os
cgitb.enable()
from jinja2 import Template, Environment, FileSystemLoader

import os, sys
import imp
import constants
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
constants = imp.load_source('modulename', 'constants.py')
import random

print("Content-type: text/html")
print()
print("<br>")
# Create instance of FieldStorage
form_data = cgi.FieldStorage()

# Get data from fields

#userid= form_data["uid"].value
First_Name = str(form_data["first_Name"].value)
Last_Name = str(form_data["last_name"].value)
Email = str(form_data["email"].value)
Username = str(form_data["uname"].value)
Password = str(form_data["psw1"].value)
#Password= str(form_data["psw2"].value)
Phone= str(form_data["phone_no"].value)


import pymysql
from pymysql.err import MySQLError
if len(Password)>8 and len(Phone)==10 :
    def hash_password(password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    new_password = hash_password(Password)
    salt = new_password[:64]

    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = constants.apiLoginId
    merchantAuth.transactionKey = constants.transactionKey


    createCustomerProfile = apicontractsv1.createCustomerProfileRequest()
    createCustomerProfile.merchantAuthentication = merchantAuth
    createCustomerProfile.profile = apicontractsv1.customerProfileType(Username, First_Name, Email)

    controller = createCustomerProfileController(createCustomerProfile)
    controller.execute()

    response = controller.getresponse()
     
    customer_profile_id = response.customerProfileId
    #print(customer_profile_id)

    conn = pymysql.connect(
         db='pyb83',
        user='pyb83',
        passwd='qeAYUn4I',
        host='localhost')
    c = conn.cursor()


    try:
      
        sql = 'INSERT INTO SIGNUP(first_name,last_name,email_id,phone_number,username,password,salt_value) VALUES("%s", "%s", "%s","%s","%s","%s","%s")' %(First_Name,Last_Name,Email,Phone,Username,new_password,salt)
        #print(sql)
        c.execute(sql)
        conn.commit()
        sql1 = 'INSERT INTO payment_info(username,customer_profile_id) VALUES("%s","%d")' %(Username,customer_profile_id)
        #print(sql1)
        c.execute(sql1)
        conn.commit()
        
    except MySQLError as e:
        print('Got error {!r}, errno is {}'.format(e, e.args[0])) 
      

    '''env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('output.html')
    output_from_parsed_template = template.render(salt=salt,new_password=new_password,fname=First_Name,lname=Last_Name,uname=Username,email=Email)

    try:
        fh = open("output.html", "w")
        fh.write(output_from_parsed_template)
    except IOError:
        print ("<br>Error: can't find file or read data")
    else:
        #print ("Written content in the file successfully")
        pass'''
    #print("Content-type:text/html\n\n")
    redirectURL = "http://pyb83.specind.net/home.html"
else:
    redirectURL = "http://pyb83.specind.net/register.html"

print("<html>")
print("<head>")
print('<meta http-equiv="refresh" content="0;url='+str(redirectURL)+'" />')
print("</head>")
print ("</html>")





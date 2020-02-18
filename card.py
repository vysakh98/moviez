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
cardnumber = str(form_data["card"].value)
cvv = str(form_data["cvv"].value)
expirationDate=str(form_data["expiry"].value)
name=str(form_data["name"].value)
import pymysql
from pymysql.err import MySQLError


conn = pymysql.connect(
    db='pyb83',
    user='pyb83',
    passwd='qeAYUn4I',
    host='localhost')
c = conn.cursor()
sql='SELECT COUNT(*) FROM SIGNUP WHERE first_name="%s"' %(name)
c.execute(sql) 
user_count=c.fetchone()
conn.commit()
if len(cardnumber)==16 and user_count[0]!=0:
  sql1= 'select username from SIGNUP where first_name="%s"' %(name)
  c.execute(sql1)
  row1 = c.fetchone()
  username = row1[0]
  conn.commit()
  sql2= 'select customer_profile_id from payment_info where username="%s"' %(username)
  c.execute(sql2)
  row2 = c.fetchone()
  customer_profile_id = row2[0]
  conn.commit()
  merchantAuth = apicontractsv1.merchantAuthenticationType()
  merchantAuth.name = constants.apiLoginId
  merchantAuth.transactionKey = constants.transactionKey

  creditCard = apicontractsv1.creditCardType()
  creditCard.cardNumber = cardnumber
  creditCard.expirationDate = expirationDate

  payment = apicontractsv1.paymentType()
  payment.creditCard = creditCard

  billTo = apicontractsv1.customerAddressType()
  billTo.firstName = name

  profile = apicontractsv1.customerPaymentProfileType()
  profile.payment = payment
  profile.billTo = billTo


  createCustomerPaymentProfile = apicontractsv1.createCustomerPaymentProfileRequest()
  createCustomerPaymentProfile.merchantAuthentication = merchantAuth
  createCustomerPaymentProfile.paymentProfile = profile

  createCustomerPaymentProfile.customerProfileId = str(customer_profile_id)

  controller = createCustomerPaymentProfileController(createCustomerPaymentProfile)
  controller.execute()

  response = controller.getresponse()

  paymentprofileid=response.customerPaymentProfileId
  sql3 = 'update payment_info set payment_id = "%s" where username="%s"' %(paymentprofileid,username)
  c.execute(sql3)
  conn.commit()
  env = Environment(loader=FileSystemLoader('templates'))
  template = env.get_template('output.html')
  output_from_parsed_template = template.render(id=paymentprofileid,user=name)

  try:
    fh = open("output.html", "w")
    fh.write(output_from_parsed_template)
  except IOError:
    print ("<br>Error: can't find file or read data")
  redirectURL = " http://pyb83.specind.net/output.html"

else:
  redirectURL = " http://pyb83.specind.net/Register.html"

print("Content-type:text/html\n\n")
print("<html>")
print("<head>")
print('<meta http-equiv="refresh" content="0;url='+str(redirectURL)+'" />')
print("</head>")
print("</html>")
      


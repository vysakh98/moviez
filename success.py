#!/usr/bin/python3 

import os, sys, cgi
import imp
import constants
import cgitb; cgitb.enable()
from jinja2 import Template, Environment, FileSystemLoader
import json
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
constants = imp.load_source('modulename', 'constants.py')
from decimal import *
import pymysql
from pymysql.err import MySQLError

print("Content-Type: text/html")
print()
print("<br>")
form = cgi.FieldStorage()

customerProfileId=form['customer_profile_id'].value
paymentProfileId= form['payment_profile_id'].value
amount = '1.32'

conn = pymysql.connect(
    db='pyb83',
    user='pyb83',
    passwd='qeAYUn4I',
    host='localhost')
c = conn.cursor()
sql1='SELECT customer_profile_id FROM `payment_info` WHERE username="%s"'
c.execute(sql1 %customerProfileId)
row=c.fetchone()
profileid=row[0]
conn.commit()


merchantAuth = apicontractsv1.merchantAuthenticationType()
merchantAuth.name = constants.apiLoginId
merchantAuth.transactionKey = constants.transactionKey


    # create a customer payment profile
profileToCharge = apicontractsv1.customerProfilePaymentType()
profileToCharge.customerProfileId = profileid
profileToCharge.paymentProfile = apicontractsv1.paymentProfile()
profileToCharge.paymentProfile.paymentProfileId = paymentProfileId

transactionrequest = apicontractsv1.transactionRequestType()
transactionrequest.transactionType = "authCaptureTransaction"
transactionrequest.amount = amount
transactionrequest.profile = profileToCharge


createtransactionrequest = apicontractsv1.createTransactionRequest()
createtransactionrequest.merchantAuthentication = merchantAuth
createtransactionrequest.refId = "MerchantID-0001"

createtransactionrequest.transactionRequest = transactionrequest
createtransactioncontroller = createTransactionController(createtransactionrequest)
createtransactioncontroller.execute()

response = createtransactioncontroller.getresponse()

transaction_id = response.transactionResponse.transId
#print(transaction_id)
#desc = response.transactionResponse.messages.message[0].description
sql2="INSERT INTO booking ()"
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('success.html')
output_from_parsed_template = template.render(trans_id =transaction_id )

try:
    fh = open("templates/success.html", "w") 
    fh.write(output_from_parsed_template)
except IOError:
    print ("<br>Error: can\'t find file or read data")
else:
    #print ("Written content in the file successfully")
    pass
#print('Content-type:text/html\n\n')
redirectURL = "http://pyb83.specind.net/templates/success.html"
print('<html>')
print('<head>')
print('<meta http-equiv="refresh" content="0;url='+str(redirectURL)+'" />') 
print('</head>')
print('</html>')   
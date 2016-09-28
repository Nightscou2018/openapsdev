#!/usr/bin/python2

# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
 
# Find these values at https://twilio.com/user/account

ACCOUNT_SID = "ACd9a1df064a9e4d939881b1c86adf28ec" # Your Account SID from www.twilio.com/console
AUTH_TOKEN  = "f083322a99bd62b673649c97a2bc6381"  # Your Auth Token from www.twilio.com/console
TO_NUMBER = "+12069484838"
FROM_NUMBER = "+14259708696" 

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
 
message = client.messages.create(to=TO_NUMBER, from_=FROM_NUMBER,
                                     body="Hello there!")

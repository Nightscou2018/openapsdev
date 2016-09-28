#!/usr/bin/python3
# check if no loop-successful file exists in this directory or if the time since it was touched is too much
# if either is true, run through removing the openaps directory, cloning in git, and sudo rebooting

import os

hostname = "www.google.com" #example
response = os.system("ping -c 1 " + hostname)

#and then check the response...
if response == 0:
  print (hostname, 'is up!')
else:
  print (hostname, 'is down!')

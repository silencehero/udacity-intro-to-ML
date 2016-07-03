#!/usr/bin/python

import os
import sys
import zipfile
from poi_flag_email import poiFlagEmail, getToFromStrings

data_dict = {}

with zipfile.ZipFile('emails.zip', "r") as z:
    z.extractall()

# make sure to aggregate count over all emails from POI to person
#   by counting all messages that are flagged as from_poi == True
for email_message in os.listdir("emails"):
    if email_message == ".DS_Store":
        continue
    message = open(os.getcwd()+"/emails/"+email_message, "r")

    to_addresses, from_addresses, cc_addresses = getToFromStrings(message)

    to_poi, from_poi, cc_poi = poiFlagEmail(message)

    for recipient in to_addresses:  # run through all recipients
        # initialize counter
        if recipient not in data_dict:  # initialize nested dict for that person
            data_dict[recipient] = {"from_poi_to_this_person":0}
        # add to count
        if from_poi:
            data_dict[recipient]["from_poi_to_this_person"] += 1

    message.close()

for item in data_dict:
    print item, data_dict[item]

#######################################################
def submitData():
    return data_dict
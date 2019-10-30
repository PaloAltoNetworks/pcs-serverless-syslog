"""
A cloud function to forward Prisma Cloud webhook messages to syslog
"""
#
# main() will be run when you invoke this action
#

import sys
import logging
import logging.handlers
import socket
import json
import requests

#Select either Syslog or Webhook destination
#OUTPUT = <webhook or syslog>
OUTPUT = "syslog"

#Insert Syslog server info 
SYSLOG_HOST = "XXX.XXX.XXX.XXX"
SYSLOG_PORT = 514

#Insert Webhook URL information 
#webhook_url = 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'



def main(request):
	request_json = request.get_json(silent=True)
    if(OUTPUT == "syslog"): 
	    syslogger = logging.getLogger('MySysLogger')
	    syslogger.setLevel(logging.INFO)
	    handler = logging.handlers.SysLogHandler(address = (SYSLOG_HOST, SYSLOG_PORT),facility = logging.handlers.SysLogHandler.LOG_LOCAL3,socktype=socket.SOCK_STREAM)
	    syslogger.addHandler(handler)
	    for alert in range(len(request_json)):
       		syslogger.info(json.dumps(request_json[alert]))
	elif(OUTPUT == webhook):
		for alert in range(len(request_json)):
       		response = requests.post(webhook_url, data=json.dumps(request_json[alert]),headers={'Content-Type': 'application/json'})

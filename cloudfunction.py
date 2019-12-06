"""
A cloud function to forward Prisma Cloud webhook messages to syslog
"""
#
# main() will be run when you invoke this action
#

import logging
import sys
import logging.handlers
import socket
import json
import requests

SYSLOG_HOST = "123.456.789.012"
SYSLOG_PORT = 514
DEST_WEBHOOK = "https://webhook.site/79a10feb-a432-475b-87c2-d85ce129a1d9"
#Set to SYSLOG or WEBHOOK
DEST_TYPE = "SYSLOG"

def main(request):
    request_json = request.get_json(silent=True)
    #Use below for SYSLOG
    if (DEST_TYPE=="SYSLOG"):
        syslogger = logging.getLogger('MySysLogger')
        syslogger.setLevel(logging.INFO)
        handler = logging.handlers.SysLogHandler(address = (SYSLOG_HOST, SYSLOG_PORT),facility = logging.handlers.SysLogHandler.LOG_LOCAL3,socktype=socket.SOCK_STREAM)
        handler.setFormatter(logging.Formatter('%(message)s\n'))
        handler.append_nul = False
        syslogger.addHandler(handler)    
        for alert in range(len(request_json)):
            syslogger.info(json.dumps(request_json[alert]))
    #Else use below for WEBHOOK
    elif (DEST_TYPE=="WEBHOOK"):
        for alert in range(len(request_json)):
            s = requests.Session()
            response = s.post(DEST_WEBHOOK, data=json.dumps(request_json[alert]), headers={'Content-Type': 'application/json'})   
            if response.status_code != 200:
                raise ValueError('Request to Webhook returned an error %s, the response is:%s' % (response.status_code, response.text))

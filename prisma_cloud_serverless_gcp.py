"""
A GCP cloud function to forward Prisma Cloud webhook messages to syslog
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

def main(request):
    request_json = request.get_json(silent=True)
    syslogger = logging.getLogger('MySysLogger')
    syslogger.setLevel(logging.INFO)
    handler = logging.handlers.SysLogHandler(address = (SYSLOG_HOST, SYSLOG_PORT),facility = logging.handlers.SysLogHandler.LOG_LOCAL3,socktype=socket.SOCK_STREAM)
    handler.setFormatter(logging.Formatter('%(message)s\n'))
    handler.append_nul = False
    syslogger.addHandler(handler)    
    for alert in range(len(request_json)):
        syslogger.info(json.dumps(request_json[alert]))

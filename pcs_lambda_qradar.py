"""
An AWS Lambda function to forward Prisma Cloud webhook messages to syslog
"""


import json
import logging
import sys
import logging.handlers
import socket
from botocore.vendored import requests

SYSLOG_HOST = "123.456.789.012"
SYSLOG_PORT = 514

def lambda_handler(event, context):
    request_json = json.loads(event['body'])
    syslogger = logging.getLogger('MySysLogger')
    syslogger.setLevel(logging.INFO)
    handler = logging.handlers.SysLogHandler(address = (SYSLOG_HOST, SYSLOG_PORT),facility = logging.handlers.SysLogHandler.LOG_LOCAL3,socktype=socket.SOCK_STREAM)
    handler.setFormatter(logging.Formatter('%(message)s\n'))
    handler.append_nul = False
    syslogger.addHandler(handler)    
    for alert in request_json:
        if 'resource' in alert:
            if 'data' in alert['resource']:
                del alert['resource']['data']
        syslogger.info(json.dumps(alert))
    return {
        'statusCode': 200
    }

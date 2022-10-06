import logging
import azure.functions as func
import logging.handlers
import socket
import json

SYSLOG_HOST = "10.0.0.4"
SYSLOG_PORT = 514


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    request_json = req.get_json()
    syslogger = logging.getLogger('MySysLogger')
    syslogger.setLevel(logging.INFO)
    handler = logging.handlers.SysLogHandler(address = (SYSLOG_HOST, SYSLOG_PORT),facility = logging.handlers.SysLogHandler.LOG_LOCAL3,socktype=socket.SOCK_STREAM)
    handler.setFormatter(logging.Formatter('%(message)s\n'))
    handler.append_nul = False
    syslogger.addHandler(handler)
    for alert in range(len(request_json)):
        syslogger.info(json.dumps(request_json[alert]))
    return func.HttpResponse(
        "This HTTP triggered function executed successfully.",
        status_code=200
    )

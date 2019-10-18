import sys
import logging
import logging.handlers
import socket
 
 SYSLOG_HOST = "123.456.789.101"
 SYSLOG_PORT = 514
  
  def main(request):
          request_json = request.get_json(silent=True)
              syslogger = logging.getLogger('MySysLogger')
                  syslogger.setLevel(logging.INFO)
                      handler = logging.handlers.SysLogHandler(address = (SYSLOG_HOST, SYSLOG_PORT),facility =logging.handlers.SysLogHandler.LOG_LOCAL3,socktype=socket.SOCK_STREAM)
                          syslogger.addHandler(handler)
                              syslogger.info(request_json)

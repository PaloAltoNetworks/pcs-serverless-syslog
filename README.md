# Prisma Cloud Function to Syslog 

Version: *1.0*
Author: *Eddie Beuerlein and Marc Hobson*

### Use Cases
- Can’t use AWS SQS integration because environment is Azure/GCP only
- Need to support a SIEM or other data ingestion tool that we currently don’t have a built-in integration available (currently we support Splunk, Jira and ServiceNow)
- Useful for anything that can ingest JSON data from a syslog message


### Requirements and Dependencies
- Syslog-NG, Rsyslog or equivalent: needs to support TCP delivery due to the size of the alert payload
- Serverless capability:
     - GCP Cloud Functions
     - AWS Lambda
     - Azure Functions
- SIEM/or other data ingestion tool that supports JSON based data (this could be other formats if there is a way to convert to them such as CEF or LEEF)


### Configuration
Cloud Function Setup

1. Create Function

2. (1)Name function and (2)Set Memory allocated to 128mb, (3)Set trigger to HTTP for use with a webhook.

3. (1)Use Inline Editor (2) Select “Python 3.7” (3) Paste code here (4) Configure function to 
Execute as “main”. Finish by clicking “Create”.

4. To attain the URL of the cloud function, (1) First click on the function, (2) Select “Trigger”, (3) Copy the URL for use with the Prisma Cloud webhook integration.

VM machine / Syslog Server Setup

1. Any Linux server will work for this setup, but the syslog server does need to support TCP in order to handle the large alert payload from Prisma.  Rsyslog or SyslogNG work great in this scenario.  Rsyslog will be used in the setup example.

2. Configuring rsyslog.conf file:
Add to top of file (needed to handle large JSON alert payload):
$MaxMessageSize 64k
Uncomment TCP section:
Provides TCP syslog reception
$ModLoad imtcp
$InputTCPServerRun 514
Modify local3.* to write to /var/log (this should match line 13 of appendix):
local3.*     /var/log/RedLock.log  

3. You may want to comment out the /etc/rsyslog.d/90-google.conf line as this can slow reception of the JSON messages or remove the file altogether.  NOTE this only affects GCP provided virtual machines. https://logrhythm.com/blog/troubleshooting-delayed-syslog-messages/

Prisma integration setup
1. https://docs.paloaltonetworks.com/prisma/prisma-cloud/prisma-cloud-admin/configure-external-integrations-on-prisma-cloud/integrate-prisma-cloud-with-webhooks

2. Insert Cloud Function trigger URL into the “Webhook URL” textbox

### Code needed for Serverless

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

#Prisma-CloudFunction-Syslog

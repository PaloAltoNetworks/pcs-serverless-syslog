import json
import boto3

DEST_TYPE = 'SQS'
SQS_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/012345678912/my_queue_name'


def lambda_handler(event, context):
    request_json = json.loads(event['body'])
    
    if DEST_TYPE == "SQS":
        sqs = boto3.resource('sqs')
        sqs_queue = sqs.Queue(SQS_QUEUE_URL)
        
        for alert in range(len(request_json)):
            response = sqs_queue.send_message(MessageBody=json.dumps(request_json[alert]))
    # TODO implement
    return {
        'statusCode': 200,
    }

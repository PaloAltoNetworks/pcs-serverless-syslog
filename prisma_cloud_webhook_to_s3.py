import json
import boto3
import datetime

DEST_TYPE = 'S3'
S3_BUCKET_NAME = 'XXXXXXXXXX'


def lambda_handler(event, context):
    request_json = json.loads(event['body'])
    
    if DEST_TYPE == "S3":
        s3 = boto3.resource("s3")

        for alert in range(len(request_json)):
            filename=str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.') + str('.json')
            s3.Bucket(S3_BUCKET_NAME).put_object(Key=filename, Body=json.dumps(request_json[alert]))
    return {
        'statusCode': 200,
    }

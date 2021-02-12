import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('AnnouncementTable')
        response = table.scan(Select='ALL_ATTRIBUTES')
        results =   response['Items']
        return {
            'announcement': results
        }
    except Exception as e:
        return {
            'exception' : "There is an issue with getting AnnouncementDetails"
        }

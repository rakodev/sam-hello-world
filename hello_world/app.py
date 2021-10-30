# import requests
import json
import os
import boto3
from botocore.exceptions import ClientError
# from pprint import pprint
from decimal import Decimal

# Fix error: "Object of type Decimal is not JSON serializable"
class DecimalEncoder (json.JSONEncoder):
    def default (self, obj):
       if isinstance (obj, Decimal):
           return int (obj)
       return json.JSONEncoder.default (self, obj)

# Create dynamoDB client
region_name = os.environ['REGION_NAME']
dynamodb_endpoint = os.environ['DYNAMODB_ENDPOINT']
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
dynamo = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint, region_name=region_name)
table_name = os.environ['TABLE_NAME']
# table = {}
# table = dynamo.Table(table_name)

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res, cls = DecimalEncoder),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def ddb_create_table(event, context):
    dynamo.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return respond(None, {"message": "Table "+ table_name + " is created."})

def ddb_insert_item(event, context):
    table = dynamo.Table(table_name)
    response = table.put_item(
        Item= {
            'year': 2021,
            'title': 'My first item'
        }
    )
    return respond(None, {"message": response})

def ddb_get_item(event, context):
    table = dynamo.Table(table_name)
    try:
        response = table.get_item(Key={'year': 2021})
    except ClientError as e:
        print(e.response['Error']['Message'])
    # pprint(response['Item'], sort_dicts=False)
    return respond(None, response['Item'])

def dynamodb_test(event, context):
    print("TableName: " + table_name)
    print("Region Name: " + region_name)
    print("DynamoDB Endpoint: "+ dynamodb_endpoint)
    scan_result = dynamo.scan(TableName=table_name)
    return respond(None, scan_result)
    # return respond(None, {})

def lambda_handler(event, context):
    return respond(None, {
            "message": "Hello! First Lambda function with SAM.",
            # "location": ip.text.replace("\n", "")
        })

# https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
def lambda_context(event, context):
    # get context info
    context_arn = context.invoked_function_arn
    cloudwatch_log_stream_name = context.log_stream_name
    cloudwatch_log_group_name = context.log_group_name
    lambda_request_id = context.aws_request_id
    lambda_memory_limits = context.memory_limit_in_mb
    lambda_remaining_time_in_ms = context.get_remaining_time_in_millis()
    lambda_remaining_time_in_sec = round(
        (lambda_remaining_time_in_ms / 1000), 2)

    return respond(None, {
            "Lambda function ARN": context_arn,
            "CloudWatch log stream name": cloudwatch_log_stream_name,
            "CloudWatch log group name": cloudwatch_log_group_name,
            "Lambda Request ID": lambda_request_id,
            "Lambda function memory limits in MB": lambda_memory_limits,
            "Lambda time remaining in MS": lambda_remaining_time_in_ms,
            "Lambda time remaining in Sec": lambda_remaining_time_in_sec
        })

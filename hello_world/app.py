import json
import time
import math

# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello! First Lambda function with SAM.",
            # "location": ip.text.replace("\n", "")
        }),
    }


def lambda_context(event, context):
    # get context info
    context_arn = context.invoked_function_arn
    cloudwatch_log_stream_name = context.log_stream_name
    cloudwatch_log_group_name = context.log_group_name
    lambda_request_id = context.aws_request_id
    lambda_memory_limits = context.memory_limit_in_mb
    lambda_remaining_time_in_ms = context.get_remaining_time_in_millis()
    lambda_remaining_time_in_sec = math.floor(
        lambda_remaining_time_in_ms / 1000)
    lambda_remaining_time_in_min = math.floor(
        lambda_remaining_time_in_sec / 60)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "Lambda function ARN": context_arn,
            "CloudWatch log stream name": cloudwatch_log_stream_name,
            "CloudWatch log group name": cloudwatch_log_group_name,
            "Lambda Request ID": lambda_request_id,
            "Lambda function memory limits in MB": lambda_memory_limits,
            "Lambda time remaining in MS": lambda_remaining_time_in_ms,
            "Lambda time remaining in Sec": lambda_remaining_time_in_sec,
            "Lambda time remaining in Min": lambda_remaining_time_in_min
        }),
    }

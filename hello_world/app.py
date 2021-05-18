import json

# import requests

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


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

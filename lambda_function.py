import json
import boto3
from urllib.parse import parse_qs
def lambda_handler(event, context):
    try:
        print("Received Event:")
        print(json.dumps(event))

        # Get HTTP method safely
        httpmethod = event.get('httpMethod')

        if not httpmethod:
            httpmethod = (
                event.get('requestContext', {})
                     .get('http', {})
                     .get('method')
            )

        if not httpmethod:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "No HTTP method found in event"
                })
            }

        querystring = event.get('queryStringParameters')
        formbody = event.get('body')

        return page_router(httpmethod, querystring, formbody)

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }


def page_router(httpmethod, querystring, formbody):

    if httpmethod == 'GET':

        with open('index.html', 'r') as htmlFile:
            htmlContent = htmlFile.read()

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': htmlContent
        }

    elif httpmethod == 'POST':

        insert_record(formbody)

        with open('success.html', 'r') as htmlFile:
            htmlContent = htmlFile.read()

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': htmlContent
        }

    else:
        return {
            'statusCode': 405,
            'body': json.dumps({
                'error': f'Method {httpmethod} not allowed'
            })
        }


def insert_record(formbody):

    data = parse_qs(formbody)

    table = boto3.resource('dynamodb').Table('mydb')

    table.put_item(
        Item={
            'mykey': data['email'][0],      # Primary Key
            'fname': data['fname'][0],
            'lname': data['lname'][0],
            'email': data['email'][0],
            'message': data['message'][0]
        }
    )

    return True

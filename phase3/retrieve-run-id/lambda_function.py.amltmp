import boto3
from botocore.exceptions import ClientError
import ast
import pymysql
import json

def get_secret():

    secret_name = "prod/LambdaStepCompute/phase3"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    try:
        # convert string type to dictionary
        dict_secret = ast.literal_eval(secret)

    except SyntaxError:
        dict_secret = {}

    return dict_secret


def get_max_run_id():

    #retrieve connection details
    dict_secret = get_secret()

    # Connect to the database
    connection = pymysql.connect(
        host=dict_secret['host'],
        port=3306,
        user=dict_secret['username'],
        password=dict_secret['password'],
        database=dict_secret['database_1']
        )

    try:
        # Get the max value from the RUN_ID column
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT MAX(RUN_ID) FROM {dict_secret['db1name']}")
            result = cursor.fetchone()[0]
        
        # Set the run_id variable based on the max value
        run_id = result + 1 if result is not None else 0

    finally:
        # Close the connection
        connection.close()
    
    return run_id

def handler(event, context):
    # Extract the number of repetitions from the event
    repetitions = event['repetitions']
    
    # Get the max value from the RUN_ID column
    run_id = get_max_run_id()

    # Create the iterable list in the format [[run_id, 0], [run_id, 1], [run_id, 2], ...]
    iterable = [[run_id, i] for i in range(repetitions)]

    # Create the output body
    output_body = []
    for i, entry in enumerate(iterable, start=1):
        entry_name = f"entry{i}"
        entry_value = f"{entry[0]}_{entry[1]}"
        output_body.append({entry_name: entry_value})

    # Prepare the output
    output = {'output_body': output_body}

    # Create the response
    response = {
        'statusCode': 200,
        'body': output
    }

    return response

import pymysql
import boto3
from botocore.exceptions import ClientError
import ast
import random
import time

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

def write_to_database(run_id, iteration_number, value):

    #retrieve connection details
    dict_secret = get_secret()
        
    # Connect to the database
    connection = pymysql.connect(
        host=dict_secret['host'],
        port=dict_secret['port'],
        user=dict_secret['username'],
        password=dict_secret['password'],
        database=dict_secret['database_1']
        )

    try:
        # Insert the values into the table
        with connection.cursor() as cursor:
            insert_query = f"INSERT INTO {dict_secret['db1name']} (RUN_ID, ITERATION_NUMBER,VALUE) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (run_id, iteration_number, value))
        
        # Commit the changes to the database
        connection.commit()

    finally:
        # Close the connection
        connection.close()

def handler(event, context):
    first_key = next(iter(event))
    value = event.get(first_key)

    if value:
        values = value.split('_')
        if len(values) == 2:
            run_id = values[0]
            iteration_number = values[1]
    
    # Generate a random integer between 0 and 1000
    random_number = random.randint(0, 1000)
    
    # Add a sleep delay of 600 seconds
    time.sleep(600)
    
    # Write the values to the database table
    write_to_database(run_id, iteration_number, random_number)
    
    return (f"Values written to the database - RUN_ID: {run_id}, ITERATION_NUMBER: {iteration_number}, VALUE: {random_number}")




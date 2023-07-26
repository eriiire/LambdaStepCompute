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

# Connect to RDS MySQL instance

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
    # Create t_lambda_poc_stage table
    with connection.cursor() as cursor:
        create_table_stage = '''
        CREATE TABLE t_lambda_poc_stage (
            RUN_ID INT,
            ITERATION_NUMBER INT,
            VALUE FLOAT
        )
        '''
        cursor.execute(create_table_stage)
    print("Table 't_lambda_poc_stage' created successfully.")

    # Create t_lambda_poc_output table
    with connection.cursor() as cursor:
        create_table_output = '''
        CREATE TABLE t_lambda_poc_output (
            RUN_ID INT,
            MEAN_VALUE FLOAT
        )
        '''
        cursor.execute(create_table_output)
    print("Table 't_lambda_poc_output' created successfully.")

finally:
    # Close the connection
    connection.close()

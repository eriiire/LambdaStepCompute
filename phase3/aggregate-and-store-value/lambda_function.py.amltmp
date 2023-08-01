import pymysql
import boto3
from botocore.exceptions import ClientError
import ast

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
    

def calculate_average(run_id):

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
        # Calculate the average of values with the same run_id
        with connection.cursor() as cursor:
            select_query = f"SELECT AVG(VALUE) FROM {dict_secret['db1name']} WHERE RUN_ID = %s"
            cursor.execute(select_query, (run_id,))
            result = cursor.fetchone()[0]
        
        # Handle cases where the average is NULL
        if result is None:
            average = 0
        else:
            average = float(result)

    finally:
        # Close the connection
        connection.close()
    
    return average

def write_to_database(run_id, average):
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
            insert_query = f"INSERT INTO {dict_secret['db2name']} (RUN_ID, MEAN_VALUE) VALUES (%s, %s)"
            cursor.execute(insert_query, (run_id, average))
        
        # Commit the changes to the database
        connection.commit()

    finally:
        # Close the connection
        connection.close()

def handler(event, context):

    # Extract file name from JSON using the 1st name in the JSON
    key_pair = next(iter(event))
    
    first_key = next(iter(key_pair))
    
    value = key_pair.get(first_key)

    if value:
        values = value.split('_')
        if len(values) == 2:
            run_id = values[0]

    
    # Calculate the average of values with the same run_id
    average = calculate_average(run_id)
    
    # Write the values to the database table
    write_to_database(run_id, average)
    
    return (f"Values written to the database - RUN_ID: {run_id}, MEAN_VALUE: {average}")


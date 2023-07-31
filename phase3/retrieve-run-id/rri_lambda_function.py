import boto3
from botocore.exceptions import ClientError
import ast
import pymysql
import json

from utils import get_secret


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

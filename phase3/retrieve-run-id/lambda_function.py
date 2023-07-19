import boto3
import pymysql
import json

# Connection details for the database
host = 'rds-db-1.cklt0stdp27j.us-east-1.rds.amazonaws.com'
port = 3306
username = 'admin'
password = 'rds-db-1-password'
database_name = 't_lambda_poc'
table_name = 't_lambda_poc_stage'

def get_max_run_id():
    # Connect to the database
    connection = pymysql.connect(host=host, port=port, user=username, password=password, database=database_name)

    try:
        # Get the max value from the RUN_ID column
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT MAX(RUN_ID) FROM {table_name}")
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

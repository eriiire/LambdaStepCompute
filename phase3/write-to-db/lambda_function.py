import pymysql
import boto3
import random
import time

# Connection details for the database
host = 'rds-db-1.cklt0stdp27j.us-east-1.rds.amazonaws.com'
port = 3306
username = 'admin'
password = 'rds-db-1-password'
database_name = 't_lambda_poc'
table_name = 't_lambda_poc_stage'

def write_to_database(run_id, iteration_number, value):
    # Connect to the database
    connection = pymysql.connect(host=host, port=port, user=username, password=password, database=database_name)

    try:
        # Insert the values into the table
        with connection.cursor() as cursor:
            insert_query = f"INSERT INTO {table_name} (RUN_ID, ITERATION_NUMBER, VALUE) VALUES (%s, %s, %s)"
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




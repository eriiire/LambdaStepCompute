import pymysql
import boto3

# Connection details for the database
host = 'rds-db-1.cklt0stdp27j.us-east-1.rds.amazonaws.com'
port = 3306
username = 'admin'
password = 'rds-db-1-password'
database_name = 't_lambda_poc'
table_name_input = 't_lambda_poc_stage'
table_name_output = 't_lambda_poc_output'

def calculate_average(run_id):
    # Connect to the database
    connection = pymysql.connect(host=host, port=port, user=username, password=password, database=database_name)

    try:
        # Calculate the average of values with the same run_id
        with connection.cursor() as cursor:
            select_query = f"SELECT AVG(VALUE) FROM {table_name_input} WHERE RUN_ID = %s"
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
    # Connect to the database
    connection = pymysql.connect(host=host, port=port, user=username, password=password, database=database_name)

    try:
        # Insert the values into the table
        with connection.cursor() as cursor:
            insert_query = f"INSERT INTO {table_name_output} (RUN_ID, MEAN_VALUE) VALUES (%s, %s)"
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


import boto3
from botocore.exceptions import ClientError
import ast
import pymysql
import json

from utils import get_secret

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

import pymysql

# Connection details
host = 'rds-db-1.cklt0stdp27j.us-east-1.rds.amazonaws.com'
port = 3306
username = 'admin'
password = 'rds-db-1-password'
database_name = 't_lambda_poc'

# Connect to RDS MySQL instance
connection = pymysql.connect(host=host, port=port, user=username, password=password, database=database_name)

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

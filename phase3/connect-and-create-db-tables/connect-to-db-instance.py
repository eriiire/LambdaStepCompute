import pymysql

# Connection details
host = 'rds-db-1.cklt0stdp27j.us-east-1.rds.amazonaws.com'
port = 3306
username = 'admin'
password = 'rds-db-1-password'

# Connect to RDS MySQL instance
connection = pymysql.connect(host=host, port=port, user=username, password=password)

try:
    # Get the list of databases
    with connection.cursor() as cursor:
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()

    # Print the database names
    print("Databases:")
    for db in databases:
        print(db[0])

finally:
    # Close the connection
    connection.close()


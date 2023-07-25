import json
import csv
import boto3

# Function to calculate the average of a list of numbers
def calculate_average(numbers):
    total = sum(numbers)
    average = total / len(numbers)
    return average

# Lambda function handler
def handler(event, context):
    # Check if the input is a non-empty list
    if not isinstance(event, list) or len(event) == 0:
        return {'message': 'Invalid input'}

    # Create an S3 client
    s3_client = boto3.client('s3')
    bucket_name = 'store-random-number'
    folder_route = 'generated_numbers/'

    # Retrieve the first entry from the event list
    entry = event[0]

    # Check if the entry has a 'message' key
    if 'message' not in entry:
        return {'message': 'Invalid input format'}

    # Extract the message from the entry
    message = entry['message']

    # Split the message to get the filter criteria
    filter_by = message.split('+')[0]

    # List objects in the S3 bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_route)

    # Initialize variables
    numbers = []
    count = 0

    # Iterate over the objects and retrieve the numbers
    for obj in response['Contents']:
        key = obj['Key']
        if key.startswith(filter_by) and key.endswith('.csv'):
            count += 1

            # Download the CSV file
            response = s3_client.get_object(Bucket=bucket_name, Key=key)
            data = response['Body'].read().decode('utf-8')

            # Parse the CSV data and extract the numbers
            reader = csv.reader(data.splitlines())
            rows = list(reader)
            numbers += [int(row[0]) for row in rows]

    # Calculate the average
    if count > 0:
        average = calculate_average(numbers)
        return {'message': f"Average of {count} files: {average}"}
    else:
        return {'message': 'No matching files found'}


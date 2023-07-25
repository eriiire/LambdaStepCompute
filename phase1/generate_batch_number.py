#import necessary libraries

import boto3
import csv
import random
import string
import time

# Create an S3 client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    
    """
    input for the function must be in the format {'repetitions':int}, 
    where `int` is the number of the times the simulation is to be run.
    
    """
    
    # Extract the number of repetitions from the event
    repetitions = event['repetitions']
    
    # Generate a unique identifier for the batch with a timestamp
    batch_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    timestamp = str(int(time.time()))
    batch_number = f'{batch_id}_{timestamp}'
    
    # Create a list to store the CSV name-value pairs
    csv_name = []
    
    # Generate name-value pairs based on the repetitions
    for i in range(repetitions):
        name = f'name{i+1}'
        value = f'{batch_number}+{i}'
        csv_name.append({name: value})
    
    # Prepare the output
    output = {'csv_name': csv_name}
    
    # Return the response with statusCode 200 and the output body
    return {
        'statusCode': 200,
        'body': output
    }


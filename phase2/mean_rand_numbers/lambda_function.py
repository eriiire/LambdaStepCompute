import json
import random
import csv
import boto3
import tempfile
import time

def handler(event, context):
    try:
        # Extract file name from JSON using the 1st name in the JSON
        name = event[next(iter(event))]
        
        # Generate a random number
        result = random.randint(0, 1000)
        
        # Time delay
        time.sleep(600)
    
        # Create a CSV file with the random number
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            file_name = temp_file.name
            writer = csv.writer(temp_file)
            writer.writerow([result])
    
        # Save the CSV file to S3
        s3_client = boto3.client('s3')
        bucket_name = 'store-random-number'
        folder_route = 'generated_numbers/'
        s3_key = folder_route + name + '.csv'
    
        with open(file_name, 'rb') as f:
            s3_client.upload_fileobj(f, bucket_name, s3_key)
    
        return {'message': f"{s3_key} has been saved in the S3 bucket."}

    except KeyError as ke:
        return {'message': f"KeyError: {ke}"}

    except ValueError as ve:
        return {'message': f"ValueError: {ve}"}

    except FileNotFoundError as fnfe:
        return {'message': f"FileNotFoundError: {fnfe}"}

    except Exception as e:
        # Handle any other unexpected exceptions
        return {'message': f"An error occurred: {e}, {file_name}"}


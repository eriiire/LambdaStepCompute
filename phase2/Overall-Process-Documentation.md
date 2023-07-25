Overall Process Documentation - AWS Step Function Workflow

Glossary of Terms

Batch Numbers: These are unique identifiers assigned to specific sets of data (in this case, random numbers) produced during each operation. They are essential for ensuring individual identification and facilitating efficient data retrieval for data aggregation purposes.

S3: Simple storage service - stores data within buckets

Introduction
This documentation outlines the overall process of the AWS Step Function workflow to orchestrate the execution of three AWS Lambda functions. The Step Function coordinates the creation of batch numbers, parallel processing of generating random numbers, creating CSV files to store the numbers, and saving the CSV files in S3 buckets, and collection of data from an S3 bucket. The primary purpose of this process is to generate and process random numbers, save them as CSV files, and calculate their average using parallelization.

Architecture Overview

![Step Function Workflow Diagram](https://github.com/eriiire/LambdaStepCompute/raw/b1a2c424f10074c581f7baeff8b9b9db553b70fe/phase2/stepfunction-workflow.png)

The process involves the following components:

AWS Step Function: The orchestrator that coordinates the execution of Lambda functions and manages the flow of data between them.

AWS Lambda Functions:

Lambda Function 1: Generates unique batch numbers and name-value pairs. These values are iterated over and passed to the 'Lambda Function 2' and used to name individual csv files.

Lambda Function 2: Generates random numbers, saves them as CSV files, and uploads them to an S3 bucket.

Lambda Function 3: Collects the generated CSV files from the S3 bucket, extracts numbers, and calculates their average.

Amazon S3 Bucket: Stores the generated CSV files containing random numbers.

Step Function Workflow
The Step Function workflow comprises the following states:

State 1: Lambda Invoke – generate_batch_number.py
Purpose: Invokes Lambda Function 1 to create batch numbers for individual CSV files and generate name-value pairs for parallel processing.

Input: Requires input in the format {'repetitions': int}, where int specifies the number of times the simulation is to be run.

Output: Returns a list of name-value pairs, each representing a batch ID and a unique identifier for the CSV file.

Retry: In case of specific Lambda errors (e.g., "Lambda.ServiceException," "Lambda.AWSLambdaException," "Lambda.SdkClientException," "Lambda.TooManyRequestsException"), the state will retry up to 6 times with an exponential backoff rate of 2 seconds between retries.

Next State: Parallel Map State.

State 2: Parallel Map - mean_rand_numbers.py
Purpose: Processes the list of name-value pairs in parallel by invoking Lambda Function 2 for each item (batch) in the list.

Input: Receives the output from the previous state (list of name-value pairs).

Output: This passes the batch id as output to the next state in the step function.

Lambda Function: Lambda Function 2 generates random numbers, creates CSV files, and uploads them to the S3 bucket. These are all done in parallel.

End State: This state is the last state for parallel processing.

State 3: Lambda Invoke - collect_file_from_s3_bucket.py
Purpose: Collects CSV files from the S3 bucket based on the processed data and batch number generated in Lambda Function 1. Then, calculates the average of the numbers extracted from the CSV files.

Input: Receives the filtered filenames from the parallel Map state and uses that to filter through the s3 bucket and select the appropriate files.

Output: Returns the average of the extracted numbers from the CSV files.

Retry: In case of specific Lambda errors (e.g., "Lambda.ServiceException," "Lambda.AWSLambdaException," "Lambda.SdkClientException," "Lambda.TooManyRequestsException"), the state will retry up to 6 times with an exponential backoff rate of 2 seconds between retries.

Next State: Success State.

State 4: Success
Purpose: Marks the successful completion of the Step Function workflow. Provided all prior steps are succesfully completed, else failure.

Input: None.

Output: None.

Workflow Summary
The Step Function is triggered with input data specifying the number of repetitions for the simulation. This determines the number of parallel processes which will be triggered.

The "Lambda Invoke" state generates batch numbers and name-value pairs for the individual CSV files.

The generated name-value pairs are processed in parallel by the "Parallel Map" state, where the second Lambda function generates random numbers, creates CSV files, and uploads them to the S3 bucket.

After parallel processing, the "Lambda Invoke (Collect Files from S3)" state collects the relevant CSV files from the S3 bucket based on the processed data and calculates the average of the extracted numbers.

The Step Function reaches the "Success" state, indicating the successful completion of the entire process.

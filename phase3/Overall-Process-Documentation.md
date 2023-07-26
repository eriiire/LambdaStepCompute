# Overall Process Documentation - AWS Step Function Workflow 

  

## Introduction 

This documentation outlines the overall process of the AWS Step Function workflow to orchestrate the execution of three AWS Lambda functions. The Step Function coordinates the creation of batch numbers, parallel processing of generating random numbers, storing the generated numbers in a relational database, and retrieval of data from the database. The primary purpose of this process is to generate and process random numbers, save them as in a database, and calculate their average using parallelization capabilities. 

  

## Architecture Overview 

![Step Function Workflow Diagram](https://github.com/eriiire/LambdaStepCompute/raw/b1a2c424f10074c581f7baeff8b9b9db553b70fe/phase2/stepfunction-workflow.png)

The process involves the following components: 

  

1. AWS Step Function: The orchestrator that coordinates the execution of Lambda functions and manages the flow of data between them. 

  

2. AWS Lambda Functions: 

   - **Lambda Function 1:** Generates unique batch numbers and name-value pairs. 

   - **Lambda Function 2:** Generates random numbers, saves them as CSV files, and uploads them to an S3 bucket. 

   - **Lambda Function 3:** Collects the generated CSV files from the S3 bucket, extracts numbers, and calculates their average. 

  

3. Amazon S3 Bucket: Stores the generated CSV files containing random numbers. 

  

## Step Function Workflow 

The Step Function workflow comprises the following states: 

  

### State 1: Lambda Invoke – generate_batch_number.py

- Purpose: Invokes Lambda Function 1 to create batch numbers for individual CSV files and generate name-value pairs for parallel processing. 

- Input: Requires input in the format `{'repetitions': int}`, where `int` specifies the number of times the simulation is to be run. 

- Output: Returns a list of name-value pairs, each representing a batch ID and a unique identifier for the CSV file. 

- Retry: In case of specific Lambda errors (e.g., "Lambda.ServiceException," "Lambda.AWSLambdaException," "Lambda.SdkClientException," "Lambda.TooManyRequestsException"), the state will retry up to 6 times with an exponential backoff rate of 2 seconds between retries. 

- Next State: Parallel Map State. 

  

### State 2: Parallel Map - mean_rand_numbers.py 

 

- Purpose: Processes the list of name-value pairs in parallel by invoking Lambda Function 2 for each item (batch) in the list.

- Input: Receives the output from the previous state (list of name-value pairs). 

- Output: None (Parallel processing). 

- Lambda Function: Lambda Function 2 generates random numbers, creates CSV files, and uploads them to the S3 bucket. These are all done in parallel.
  
- End State: This state is the last state for parallel processing. 

  

### State 3: Lambda Invoke - collect_file_from_s3_bucket.py 

 

- Purpose: Collects CSV files from the S3 bucket based on the processed data and batch number generated in Lambda Function 1. Then, calculates the average of the numbers extracted from the CSV files.

- Input: Receives the filtered filenames from the parallel Map state and uses that to filter through the s3 bucket and select the appropriate files. 

- Output: Returns the average of the extracted numbers from the CSV files. 

- Retry: In case of specific Lambda errors (e.g., "Lambda.ServiceException," "Lambda.AWSLambdaException," "Lambda.SdkClientException," "Lambda.TooManyRequestsException"), the state will retry up to 6 times with an exponential backoff rate of 2 seconds between retries. 

- Next State: Success State. 

  

### State 4: Success 

- Purpose: Marks the successful completion of the Step Function workflow. Provided all prior steps are succesfully completed, else failure.

- Input: None. 

- Output: None. 

  

## Workflow Summary 

1. The Step Function is triggered with input data specifying the number of repetitions for the simulation. This determines the number of parallel processes which will be triggered.  

2. The "Lambda Invoke 1" state generates batch numbers and name-value pairs for the individual CSV files. 

3. The generated name-value pairs are processed in parallel by the "Parallel Map" state, where Lambda Function 2 generates random numbers, creates CSV files, and uploads them to the S3 bucket. 

4. After parallel processing, the "Lambda Invoke 3 (Collect Files from S3)" state collects the relevant CSV files from the S3 bucket based on the processed data and calculates the average of the extracted numbers. 

5. The Step Function reaches the "Success" state, indicating the successful completion of the entire process. 

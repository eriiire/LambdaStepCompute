# Overall Process Documentation - AWS Step Function Workflow

## Introduction

This documentation outlines the overall process of the AWS Step Function workflow to orchestrate the execution of three AWS Lambda functions. The Step Function coordinates the creation of batch numbers, parallel processing of generating random numbers, inserting the generated random numbers in a relational database, then collection and aggregation of data from the database.

## Architecture Overview

![Step Function Workflow Diagram](https://github.com/eriiire/LambdaStepCompute/raw/b1a2c424f10074c581f7baeff8b9b9db553b70fe/phase2/stepfunction-workflow.png)

The process involves the following components:

1. AWS Step Function: The orchestrator that coordinates the execution of Lambda functions and manages the flow of data between them.

2. AWS Lambda Functions:

   - **Lambda Function 1 (retrieve-run-id.py):** Generates unique run IDs and iteration IDs.
   - **Lambda Function 2 (write-to-db.py):** Generates random numbers, saves them to the database, and introduces a 10-minute sleep delay for each iteration.
   - **Lambda Function 3 (aggregate-and-store-value.py):** Collects the generated values from the database, calculates their average, and stores it in another database.

3. Amazon RDS Database: Stores the generated values and their corresponding run and iteration IDs.

## Step Function Workflow

The Step Function workflow comprises the following states:

### State 1: Lambda Invoke 1 - retrieve-run-id.py

- Purpose: Invokes Lambda Function 1 to create run and iteration IDs which will be iterated over for parallel processing.
- Input: Requires input in the format `{'repetitions': int}`, where `int` specifies the number of times the simulation is to be run.
- Output: Returns a json of run_id-iteration_id pairs, each representing a unique identifier for the random number generated.
- Retry: In case of specific Lambda errors (e.g., "Lambda.ServiceException," "Lambda.AWSLambdaException," "Lambda.SdkClientException," "Lambda.TooManyRequestsException"), the state will retry up to 6 times with an exponential backoff rate of 2 seconds between retries.
- Next State: Parallel Map State.

### State 2: Parallel Map - Lambda Invoke 2 - write-to-db.py

- Purpose: Processes the json of run_id-iteration_id pairs in parallel by invoking Lambda Function 2 for each item (batch) in the list.
- Input: Receives the output from the previous state
- Output: None (Parallel processing).
- Lambda Function: Lambda Function 2 generates random numbers, introduces a 10-minute sleep delay for each iteration, and writes the values to the database. These operations are performed in parallel.
- End State: This state is the last state for parallel processing.

### State 3: Pass

- Purpose: Passes the output from the Parallel Map state to the Lambda Invoke 3 state.
- Input: Receives the list of processed run_id-iteration_id pairs from the Parallel Map state.
- Next State: Lambda Invoke 3.

### State 4: Lambda Invoke 3 - aggregate-and-store-value.py

- Purpose: Collects values from the database based on the processed data and run ID generated in Lambda Function 1. Then, calculates the average of the values extracted from the database.
- Input: Receives the list of processed run_id-iteration_id pairs from the Pass state and uses the run ID to fetch the corresponding values from the database.
- Output: Returns the average of the extracted values from the database.
- Retry: In case of specific Lambda errors (e.g., "Lambda.ServiceException," "Lambda.AWSLambdaException," "Lambda.SdkClientException," "Lambda.TooManyRequestsException"), the state will retry up to 6 times with an exponential backoff rate of 2 seconds between retries.
- Next State: Success State.

### State 5: Success

- Purpose: Marks the successful completion of the Step Function workflow. Provided all prior steps are successfully completed; otherwise, the state machine will fail.
- Input: None.
- Output: None.

## Workflow Summary

1. The Step Function is triggered with input data specifying the number of repetitions for the simulation. This determines the number of parallel processes that will be triggered.

2. The "Lambda Invoke 1" state generates run id and iteration id pairs for the generated random numbers.

3. The generated run_id-iteration-id pairs are processed in parallel by the "Parallel Map" state, where Lambda Function 2 generates random numbers, introduces a 10-minute sleep delay for each iteration, and writes the values to the database.

4. After parallel processing, the "Pass" state passes the relevant data to the "Lambda Invoke 3 (Calculate Average)" state, which collects the corresponding values from the database (all values with the same run-id), calculates the average, the writes it to a different table in the database.

5. The Step Function reaches the "Success" state, indicating the successful completion of the entire process.

### Presentation on a Proof of Concept for Parallelisation of the WSSR Project

---

#### Introduction

This project aims to execute provide a POC for the parallelisation of the WSSR Project, the project can be divided into two parts:

- **LambdaStepCompute:** Using AWS Lambda Functions and Step Functions to explore the possibility of executing operations in parallel integrating a storage solution into the workflow process.
  
- Splitting the WSSR code, into two chunks and running both individually:
  - The Simulation Chunk: This segment focuses on the execution of the simmer simulation repeatedly. Each iteration's resultant data is preserved as rds objects.
  
  - The Collation and Output Chunk: This segment is concerned with the merging of individual simulation outputs. It ends with the creation of a unified object. This then follows the previous flow and is undergoes output wrangling to produce a CSV file.

---

### LambdaStepCompute

---

#### Objectives

- To run R code N times in parallel (currently 10, but scalable for the future).
- To aggregate the results of these runs.
- To explore options for running R code in AWS Lambda functions.

---

#### Architecture Overview

The architecture involves the following components:

1. **AWS Step Function**: Orchestrates the execution of Lambda functions and manages the flow of data between them.
2. **AWS Lambda Functions**: Perform specific tasks like generating batch numbers, creating CSV files, and calculating averages.
3. **Amazon S3 Bucket**: Stores the generated CSV files containing random numbers.

![Step Function Workflow Diagram](https://github.com/eriiire/LambdaStepCompute/raw/b1a2c424f10074c581f7baeff8b9b9db553b70fe/phase2/stepfunction-workflow.png)

---

#### Workflow

1. **State 1: Lambda Invoke – generate_batch_number.py**
    - Generates unique batch numbers and name-value pairs.
    - Input: `{'repetitions': int}`
    - Output: List of name-value pairs.
  
2. **State 2: Parallel Map - mean_rand_numbers.py**
    - Processes the list of name-value pairs in parallel.
    - Input: Output from the previous state.
    - Output: None (Parallel processing).
  
3. **State 3: Lambda Invoke - collect_file_from_s3_bucket.py**
    - Collects CSV files from the S3 bucket and calculates their average.
    - Input: Filtered filenames from the parallel Map state.
    - Output: Average of the extracted numbers.

4. **State 4: Success**
    - Marks the successful completion of the Step Function workflow.

---

#### Proof of Concept (Phase 1)

1. **Python Script 1 (generate_batch_number.py)**: Generates unique batch numbers and name-value pairs.
2. **Python Script 2 (mean_rand_numbers.py)**: Generates random numbers, saves them as CSV files, and uploads them to an S3 bucket.
3. **Python Script 3 (collect_file_from_s3_bucket.py)**: Collects the generated CSV files from the S3 bucket, extracts the numbers, and calculates their average.

This phase mimics the individual runs and runtime of the WSM code. These Python scripts are executed using workflows orchestrated by AWS Step Functions. Each iteration of Python Script 2 is run in parallel.

---

#### ARN References

- `generate_batch_number`: `arn:aws:lambda:us-east-1:066035006373:function:generate_batch_number:$LATEST`
- `mean_rand_numbers`: `arn:aws:lambda:us-east-1:066035006373:function:mean_rand_numbers:$LATEST`
- `collect_file_from_s3_bucket`: `arn:aws:lambda:us-east-1:066035006373:function:collect_file_from_s3_bucket:$LATEST`

---

#### Code Snippets

- [generate_batch_number.py](https://github.com/eriiire/LambdaStepCompute/blob/main/phase1/generate_batch_number.py)
- [mean_rand_numbers.py](https://github.com/eriiire/LambdaStepCompute/blob/main/phase1/mean_rand_numbers.py)
- [collect_file_from_s3_bucket.py](https://github.com/eriiire/LambdaStepCompute/blob/main/phase1/collect_file_from_s3_bucket.py)

---

You are currently on the free plan, which is significantly limited by the number of requests. To increase your quota, you can check available plans [here](https://c7d59216ee8ec59bda5e51ffc17a994d.auth.portal-pluginlab.ai/pricing).

Would you like to know more about any specific aspect of the project?

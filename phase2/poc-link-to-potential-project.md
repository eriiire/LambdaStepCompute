# Phase 2 Overview

In Phase 2 of this project, we build upon the work from Phase 1 and introduce Docker containers to enhance the execution environment for our Python scripts. Each Python script is now encapsulated within a Docker container, which will be utilized to create the corresponding Lambda function for smoother deployment and execution.

Since the project code may contain scripts in languages unsupported by Lambda functions (such as R), Docker containers will be used to package these scripts and create corresponding Lambda functions.

## Python Scripts and Docker Containers

1. **Python Script 1 (`generate_batch_number.py`):** This script generates unique batch numbers and name-value pairs. It is placed inside a Docker container to ensure a consistent runtime environment.

2. **Python Script 2 (`mean_rand_numbers.py`):** This script generates random numbers and introduces a 600-second delay using the `time.sleep` function. It saves the generated numbers as CSV files and uploads them to an S3 bucket. This script is containerized using Docker for reliable and reproducible execution.

3. **Python Script 3 (`collect_file_from_s3_bucket.py`):** This script collects the generated CSV files from the S3 bucket, extracts the numbers, and calculates their average. It is also packed within a Docker container for seamless integration.

This phase simulates the individual runs and runtime of the long-running code.

These Python scripts are executed using workflows orchestrated by AWS Step Functions. Each iteration of Python Script 2 is run in parallel.

## Docker Containers for Lambda Functions

To create Lambda functions from these Docker containers, please follow the instructions outlined in the file titled `create-and-deploy-dockerfile.md`. This document provides step-by-step guidance on building Docker images and deploying them as Lambda functions in AWS.

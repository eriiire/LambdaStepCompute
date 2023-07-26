# Phase 3 Overview

In Phase 3 of this project, we build upon the work from Phase 1 and Phase 2. Docker containers are still used, but instead of storing generated random numbers in csv files and s3 buckets; random numbers are instead stored in a relational database. This will be utilized for smoother deployment and retrieval of data, and will closely mirror the deployment structure of the WSM project.

## Python Scripts and Docker Containers

1. **Python Script 1 (retrieve-run-id.py):** This script generates generates unique run id's and iteration id's. It is placed inside a Docker container to ensure a consistent runtime environment.

2. **Python Script 2 (write-to-db.py):** This script generates random numbers, saves them to the database, and introduces a 10-minute sleep delay for each iteration.

3. **Python Script 3 (aggregate-and-store-value.py):** This script collects the generated values from the database, calculates their average, and stores it in a different table in the database.

This phase mimics the individual runs and runtime of the WSM code.

These Python scripts are executed using workflows orchestrated by AWS Step Functions. Each iteration of Python Script 2 is run in parallel.

## Docker Containers for Lambda Functions

To create Lambda functions from these Docker containers, please follow the instructions outlined in the file titled 'create-and-deploy-dockerfile.md'. This document provides step-by-step guidance on building Docker images and deploying them as Lambda functions in AWS.

## Relational Database

The AWS RDS MySQL database (Community Version) is used to store any data generated during this process.

Information on how to connect to AWS RDS MySQL can be found here: [How to connect to DB instance (https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToInstance.html)


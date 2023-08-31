### Presentation on a Proof of Concept for Parallelisation of the WSSR Project

---

#### Introduction

This project aims to execute provide a POC for the parallelisation of the WSSR Project, the project can be divided into two parts:

- **LambdaStepCompute:** Using AWS Lambda Functions and Step Functions to explore the possibility of executing operations in parallel integrating a storage solution into the workflow process.
  
- **wssr-model-split:** Splitting the WSSR code, into two chunks and running both individually:
  - The Simulation Chunk: This segment focuses on the execution of the simmer simulation repeatedly. Each iteration's resultant data is preserved as rds objects.
  
  - The Collation and Output Chunk: This segment is concerned with the merging of individual simulation outputs. It ends with the creation of a unified object. This then follows the previous flow and is undergoes output wrangling to produce a CSV file.

---

### LambdaStepCompute

---

#### Objectives

- To run R code N times in parallel (currently 10, but scalable for the future).
- To store the results
- To aggregate the results of these runs.
- To explore options for running R code in AWS Lambda functions.

---

![Step Function Workflow Diagram](https://github.com/eriiire/LambdaStepCompute/raw/b1a2c424f10074c581f7baeff8b9b9db553b70fe/phase2/stepfunction-workflow.png)

---

This is divided into 3 phases:

#### Phase 1: Phase 1 involves executing 3 Lambda Functions. Random numbers are generated in parallel, stored in an S3 bucket, then extracted and aggregated.

1. AWS Step Function: The orchestrator that coordinates the execution of Lambda functions and manages the flow of data between them. 

2. AWS Lambda Functions: 

   - **Lambda Function 1:** Generates unique batch numbers and name-value pairs. 

   - **Lambda Function 2:** Generates random numbers, saves them as CSV files, and uploads them to an S3 bucket. 

   - **Lambda Function 3:** Collects the generated CSV files from the S3 bucket, extracts numbers, and calculates their average. 

3. Amazon S3 Bucket: Stores the generated CSV files containing random numbers.

---

#### Phase 2: Phase 2 follows the exact workflow as Phase 1 but involves utilizing Docker containers to package the Lambda functions, which are then pushed to the Amazon Elastic Container Registry (ECR). These containers are used to create individual Lambda functions, which are then integrated into the Step Function workflow.

---

#### Phase 3: Phase 3 uses Docker containers built upon in Phase 2 but instead of storing generated random numbers in csv files and s3 buckets; random numbers are instead stored in a relational database. This will be utilized for smoother deployment and retrieval of data, and will closely mirror the deployment structure of the WSM project.

1. AWS Step Function: The orchestrator that coordinates the execution of Lambda functions and manages the flow of data between them.

2. AWS Lambda Functions:

   - **Lambda Function 1 (retrieve-run-id.py):** Generates unique run IDs and iteration IDs.
   - **Lambda Function 2 (write-to-db.py):** Generates random numbers, saves them to the database, and introduces a 10-minute sleep delay for each iteration.
   - **Lambda Function 3 (aggregate-and-store-value.py):** Collects the generated values from the database, calculates their average, and stores it in another database.

3. Amazon RDS Database: Stores the generated values and their corresponding run and iteration IDs.

---

### Conclusion on LambdaStepCompute

The Proof of Concept (POC) for the parallelization of the WSSR Project, specifically focusing on the LambdaStepCompute component, has been successful. Each phase and the steps within those phases were executed successfully to completion.

#### Phase 1: 
The initial phase demonstrated the feasibility of executing Lambda Functions in parallel, orchestrated by AWS Step Functions. All objectives were met, including the generation of random numbers, their storage in an S3 bucket, and subsequent aggregation.

#### Phase 2: 
Building upon the success of Phase 1, this phase introduced Docker containers to package the Lambda functions. The containers were successfully pushed to Amazon ECR and integrated into the Step Function workflow. This added an extra layer of flexibility and scalability to the project, proving that the architecture can adapt to more tailored requirements.

#### Phase 3: 
The final phase took the project a step further by replacing the S3 storage solution with an Amazon RDS Database. This not only streamlined the data storage and retrieval process but also closely mirrored the deployment structure of the WSM project. The introduction of a relational database made the system more aligned with deployment-level needs.

In summary, each phase and its corresponding steps have been executed successfully, meeting all set objectives. The LambdaStepCompute component has proven that it can efficiently run R code in parallel, store and aggregate results, and do so in a scalable manner. This POC serves as a foundation for the future development and deployment of the WSSR-Model Project.

---

#### Code Snippets

- [generate_batch_number.py](https://github.com/eriiire/LambdaStepCompute/blob/main/phase1/generate_batch_number.py)
- [mean_rand_numbers.py](https://github.com/eriiire/LambdaStepCompute/blob/main/phase1/mean_rand_numbers.py)
- [collect_file_from_s3_bucket.py](https://github.com/eriiire/LambdaStepCompute/blob/main/phase1/collect_file_from_s3_bucket.py)

---

You are currently on the free plan, which is significantly limited by the number of requests. To increase your quota, you can check available plans [here](https://c7d59216ee8ec59bda5e51ffc17a994d.auth.portal-pluginlab.ai/pricing).

Would you like to know more about any specific aspect of the project?

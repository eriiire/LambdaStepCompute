# LambdaStepCompute

Objective: This project aims to compute in parallel, several simulation tasks using AWS Lambda Functions and Step Functions. By leveraging the scalability and flexibility of AWS Lambda Functions and the orchestration capabilities of Step Functions, the system will maximize computational efficiency and hopefully reduce processing time for the compute-intensive task.

Stakeholders: Development team and users

Scope: Develop a proof of concept using AWS Lambda functions and Step Functions to compute simulations in parallel and aggregate the results following completion.

Deliverables: A working proof of concept using AWS Lambda functions and Step Functions to compute simulations in parallel and aggregate the results following completion.

Methodology and Approach: 
-  Create a Lambda function that generates a single random number. 
-  Configure the function to generate and store the random number in an individual JSON or CSV file. 
-  Test the function to ensure it generates random numbers accurately. 
-  Design a Step Functions workflow that chains the Lambda function calls. 
-  Configure the workflow to invoke the Lambda function 1,000 times in parallel. 
-  Each Lambda function call generates a random number and stores it in a separate file. 
-  Develop a script or Lambda function to retrieve the random numbers from the individual JSON or CSV files. 
-  Aggregate the collected numbers into a single result. 
-  Analyze and compare the performance of the proess compared to the prior process.

Success Criteria: The parallel computing system using AWS Lambda Functions and Step Functions significantly reduces the time taken to perform all simulations compared to a traditional sequential approach.

Timeline: 

# LambdaStepCompute

This project aims to compute several simulation tasks in parallel using AWS Lambda Functions and Step Functions.

In the `create-docker-test` branch, the goal is to create a Docker container image using an Azure virtual machine. The container image will contain all required libraries and the Python code to be run and tested. The container image will be pushed and deployed to an Elastic Container Repository (ECR) on the AWS platform. A Lambda function will be created using the pushed Docker containers in the Elastic Container Repository on the AWS platform. The Lambda functions will be chained together in a workflow using AWS Step Functions. The Step Functions will then be evaluated and run.

# Further Details

- The project consists of R or Python code.
- This code is run *N* times (currently 10, though this may change in the future).
- The results from these runs are aggregated.

# Current Unknowns

- How do we coordinate multiple parallel runs with Lambdas and Step Functions?
- What options are available for collating the results?
- How do we run R in the Lambdas (Docker is one possible route, hence the steps into Docker)?

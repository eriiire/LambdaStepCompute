# LambdaStepCompute
This project aims to compute in parallel, several simulation tasks using AWS Lambda Functions and Step Functions.

In the create-docker-test branch - the aim is to create a docker container image using an Azure virtual machine. 
The container image will contain all required libraries, and the python code to be run and tested.
The container image will be pushed and deployed to an Elastic Container Repository (ECR) on the AWS platform. 
A lambda function will be created using the pushed docker containers in the Elastic Container Repository on the AWS platform. 
The lambda functions will be chained together in a workflow using AWS Step Functions.
The Step Functions will be evaluated and run.

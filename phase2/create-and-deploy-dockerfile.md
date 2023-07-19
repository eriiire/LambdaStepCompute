## Creating and Deploying a Docker Image for Python Lambda Function

Prerequisites: AWS CLI, Python

### Step 1 - Create Project Directory
Create a directory for the project and navigate to that directory using the terminal.

### Step 2 - Create Lambda Function Script
Create a new file called `lambda_function.py` containing the Python script/function to be executed as the Lambda function.

### Step 3 - Define Dependencies
Create a new file called `requirements.txt` listing the required dependencies/libraries needed by the Python script. For example:

```plaintext
Boto3
pymysql
```

### Step 4 - Dockerfile Configuration
Create a new `Dockerfile` with the following configuration (use a text editor like `nano` or any other preferred editor):

```Dockerfile
FROM public.ecr.aws/lambda/python:3.10

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]
```

### Step 5 - Build the Docker Image
Build the Docker image with the `docker build` command. The example below names the image `docker-image` and gives it the `test` tag.

```bash
docker build -t docker-image:test .
```

### Deploying the Docker Build

### Step 1 - Create ECR Repository
Create a repository in the AWS Elastic Container Repository (ECR) to store the Docker image.

### Step 2 - View Push Commands
After creating the repository, access it, and click on "View Push Commands" to obtain the push commands specific to that repository.

### Step 3 - Authenticate Docker Client
Copy the authentication token and authenticate your Docker client to the ECR registry using the AWS CLI command:

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 111122223333.dkr.ecr.us-east-1.amazonaws.com
```

### Step 4 - Tag and Push Image
Tag the Docker image and push it to your created ECR repository:

```bash
docker tag docker-image:test 111122223333.dkr.ecr.us-east-1.amazonaws.com/hello-world:latest
```

### Step 5 - Push Image to ECR
Run the `docker push` command to deploy your local image to the Amazon ECR repository:

```bash
docker push 111122223333.dkr.ecr.us-east-1.amazonaws.com/hello-world:latest
```

Reference: [Deploy Python Lambda functions with container images - AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/python-image.html)

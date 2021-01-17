# aws-examples

Simple example uses of different AWS services.

<img src="https://raw.githubusercontent.com/cncf/landscape/81c02a5f231a5c0a4acfc5753d943c37040bb766/hosted_logos/amazon-web-services.svg" height="50">


## [AWS CloudFormation](https://aws.amazon.com/cloudformation/)

> _Cloud provisioning with infrastructure as code_

<img src="https://raw.githubusercontent.com/cncf/landscape/81c02a5f231a5c0a4acfc5753d943c37040bb766/hosted_logos/aws-cloudformation.svg" height="130">

1. Install [AWS Command Line Interface (CLI)](https://aws.amazon.com/cli/)

    * Configure the CLI: `aws configure`
    * [Add user for the CLI](https://console.aws.amazon.com/iam)

2. [Create SSH key pair for the EC2 instance](https://console.aws.amazon.com/ec2/home#KeyPairs)

3. Create/update/delete the CloudFormation stack:
   ```bash
   aws --region eu-north-1 cloudformation create-stack --stack-name ec2-only --template-body file://cloudformation/ec2.yaml
   aws --region eu-north-1 cloudformation update-stack --stack-name ec2-only --template-body file://cloudformation/ec2.yaml
   aws --region eu-north-1 cloudformation delete-stack --stack-name ec2-only
   ```
   
4. [Monitor the stack creation progress](https://console.aws.amazon.com/cloudformation)


## [AWS Serverless Application Model (SAM)](https://aws.amazon.com/serverless/sam/)

> _CloudFormation extension optimized for serverless applications_

<img src="https://raw.githubusercontent.com/cncf/landscape/81c02a5f231a5c0a4acfc5753d943c37040bb766/hosted_logos/aws-sam.svg" height="100">

1. Install [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
   
   ```bash
   python -m pip install aws-sam-cli
   ```
   
2. Build the AWS SAM application using [`sam build`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-build.html) command.
   
   > The `sam build` command processes your AWS SAM template file, application code, and any applicable language-specific files
   > and dependencies, and copies build artifacts in the format and location expected by subsequent steps in your workflow. 
   
   ```bash
   sam build \
       --template sam/lambda.yaml \
       --manifest sam/lambda-code/requirements.txt
   ```

3. Run our serverless application locally for quick development and testing using Docker and [`sam local start-api`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-local-start-api.html) command.

   Note: SAM CLI [doesn't support schema validation](https://github.com/aws/aws-sam-cli/issues/364) like API Gateway does,
   so we have to deploy the SAM stack to check whether the validation is working.

   ```bash
   sam local start-api
   ```
   
   Send a testing request to the API:

   ```bash
   curl \
       --header "Content-Type: application/json" \
       --request POST \
       --data '{"searchTerm": "United States"}' \
       http://localhost:3000
   ```

4. Package the AWS SAM application using [`sam package`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-package.html) command.
   
   > It creates a ZIP file of your code and dependencies, and uploads it to Amazon S3.
   > It then returns a copy of your AWS SAM template, replacing references to local artifacts with the Amazon S3 location where the command uploaded the artifacts.
   
   Before running the following command, you need to create a S3 bucket for it.
   
   ```bash
   sam package \
       --s3-bucket my-cloudformation-templates-12345 \
       --output-template-file sam/lambda-packaged.yaml
   ```
   
   TODO: is this step needed anymore? https://stackoverflow.com/a/63061658/5524090

5. Deploy the AWS SAM application using [`sam deploy`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-deploy.html) command.
   
   ```bash
   sam deploy \
       --template sam/lambda-packaged.yaml \
       --stack-name my-first-sam-stack \
       --capabilities CAPABILITY_IAM \
       --region eu-north-1
   ```


## Useful resources

* [Difference in Lambda's event parameter when the Lambda is executed directly vs. through API Gateway](https://stackoverflow.com/a/48391462/5524090)

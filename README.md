# aws-examples

Simple example uses of different AWS services.

<img src="https://raw.githubusercontent.com/cncf/landscape/81c02a5f231a5c0a4acfc5753d943c37040bb766/hosted_logos/amazon-web-services.svg" height="50">


## [AWS CloudFormation](https://aws.amazon.com/cloudformation/)

> _Cloud provisioning with infrastructure as code_

<img src="https://raw.githubusercontent.com/cncf/landscape/81c02a5f231a5c0a4acfc5753d943c37040bb766/hosted_logos/aws-cloudformation.svg" height="130">

1. Install [AWS Command Line Interface (CLI)](https://aws.amazon.com/cli/)

2. Configure the CLI: `aws configure`
    <br>
    Add user for the CLI on https://console.aws.amazon.com/iam
3. Create SSH key pair for the EC2 instance on https://console.aws.amazon.com/ec2/home#KeyPairs

4. Create/update/delete the CloudFormation stack:
   ```bash
   aws --region eu-north-1 cloudformation create-stack --stack-name ec2-only --template-body file://cloudformation/ec2.yaml
   aws --region eu-north-1 cloudformation update-stack --stack-name ec2-only --template-body file://cloudformation/ec2.yaml
   aws --region eu-north-1 cloudformation delete-stack --stack-name ec2-only
   ```
   
5. Monitor the progress at https://console.aws.amazon.com/cloudformation


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

3. Invoke our Lambda function locally using Docker and [`sam local invoke`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-local-invoke.html) command.
   
   ```bash
   sam local invoke "HelloWorldFunction"
   echo '{"searchTerm": "United States"}' | sam local invoke "HelloWorldFunction" --event -
   sam local invoke --event sam/lambda-example-query.json
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

5. Deploy the AWS SAM application using [`sam deploy`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-deploy.html) command.
   
   ```bash
   sam deploy \
       --template sam/lambda-packaged.yaml \
       --stack-name my-first-sam-stack \
       --capabilities CAPABILITY_IAM \
       --region eu-north-1
   ```

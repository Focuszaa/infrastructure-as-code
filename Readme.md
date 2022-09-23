# Automate provision AWS resources using cloudformation and Cdk

This project are having both Cloudformation template and CDK (cloud development kit) using Python. 

## Sub project list.
### Cloudformation 
- Project: CfnBaseImageBuilder, Status: 🟢 Available. cfn BaseImageBuilder Use priodically build base image for update vulnerability then use it later when build an application - the cfn provision CodePipeline with 2 stages, sources and build docker images push to ECR, there is cloudwatch event for schedule execute a pipeline as weekly, notification on codestar to notice fail/success using SNS. also having an cloudwatch event rule to execute pipeline when there is change on main branch of codecommit. 

### Cdk
- Project: CdkBaseImageBuilder, Status: 🟢 Available . CDK BaseImageBuilder Use priodically build base image for update vulnerability then use it later when build an application - the CDK provision CodePipeline with 2 stages, sources and build docker images push to ECR, there is cloudwatch event for schedule execute a pipeline as weekly, notification on codestar to notice fail/success using SNS. also having an cloudwatch event rule to execute pipeline when there is change on main branch of codecommit.

- Project: CdkBastionHost, Status: 🟡 In progress, Cdk BastionHost act as a point to connecting into inside VPC, there resources component suce as Ec2 Sg VPC Subnet KeyPair SSM 
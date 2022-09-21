# templates for provision AWS resources 

In rgis project there are both Cloudformation template and CDK (cloud development kit) using Python. 

## List of sub project inside.
### Cloudformation 
- Status: 🟢 Available. cfn BaseImageBuilder User for update vulnerability on a base image then use it later on when build an application - the cfn provision CodePipeline with 2 stages, sources and build docker images push to ECR, there is cloudwatch event for schedule execute a pipeline as weekly, notification on codestar to notice fail/success using SNS. also having an cloudwatch event rule to execute pipeline when there is change on main branch of codecommit. 

### Cdk
- Status: 🟡 InProgress. CDK BaseImageBuilder User for update vulnerability on a base image then use it later on when build an application - the CDK provision CodePipeline with 2 stages, sources and build docker images push to ECR, there is cloudwatch event for schedule execute a pipeline as weekly, notification on codestar to notice fail/success using SNS. also having an cloudwatch event rule to execute pipeline when there is change on main branch of codecommit. 
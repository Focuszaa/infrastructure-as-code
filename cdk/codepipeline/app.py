from aws_cdk import (App)

from Base import Base
from Pipeline import Pipeline

props = {'namespace': 'code-pipeline'}


app=App()

# base resources for create ecr codebuild and s3
base = Base(app, f"{props['namespace']}-base", props)

# pipeline stack 
pipeline = Pipeline(app, f"{props['namespace']}-pipeline", base.outputs)
pipeline.add_dependency(base)
app.synth()


# from base_image_pipeline.base_image_pipeline_stack import BaseImagePipelineStack


# app = cdk.App()
# BaseImagePipelineStack(app, "BaseImagePipelineStack",
#     # If you don't specify 'env', this stack will be environment-agnostic.
#     # Account/Region-dependent features and context lookups will not work,
#     # but a single synthesized template can be deployed anywhere.

#     # Uncomment the next line to specialize this stack for the AWS Account
#     # and Region that are implied by the current CLI configuration.

#     # env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

#     # Uncomment the next line if you know exactly what Account and Region you
#     # want to deploy the stack to. */

#     env=cdk.Environment(account='892456250180', region='us-east-1'),

#     # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
#     )

# app.synth()

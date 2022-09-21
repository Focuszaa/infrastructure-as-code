from aws_cdk import (App)

from Base import Base
from Pipeline import Pipeline
from EventTrigger import EventTrigger
# from cdk.codepipeline.EventTrigger import EventTrigger

props = {'projectName': 'ImageBuilder'}


app=App()

# base resources for create ecr codebuild and s3
base = Base(app, f"{props['projectName']}-base", props)

# pipeline stack 
pipeline = Pipeline(app, f"{props['projectName']}-pipeline", base.outputs)
pipeline.add_dependency(base)

#ventRule stacks
eventrule = EventTrigger(app, f"{props['projectName']}-event-rule", pipeline.outputs)
eventrule.add_dependency(pipeline)

app.synth()
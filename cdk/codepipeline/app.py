from aws_cdk import (App)

from Base import Base
from Pipeline import Pipeline

props = {'projectName': 'ImageBuilder'}


app=App()

# base resources for create ecr codebuild and s3
base = Base(app, f"{props['projectName']}-base", props)

# pipeline stack 
pipeline = Pipeline(app, f"{props['projectName']}-pipeline", base.outputs)
pipeline.add_dependency(base)
app.synth()

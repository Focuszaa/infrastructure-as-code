from aws_cdk import (
    aws_codepipeline,
    aws_codepipeline_actions,
    aws_ssm,
    App, CfnOutput, Stack
)


class Pipeline(Stack):
    def __init__(self, app: App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # defind s3 artifact
        source_output = aws_codepipeline.Artifact(artifact_name='source')

        pipeline = aws_codepipeline.Pipeline(
            self, "Pipeline",
            pipeline_name=f"{props['projectName']}",
            # pipeline_name='cdkPipeline',
            artifact_bucket=props['bucket'],
            stages=[
                aws_codepipeline.StageProps(
                  stage_name='source',
                    actions=[
                        aws_codepipeline_actions.CodeCommitSourceAction(
                            action_name="Source",
                            repository=props['cc_repo'],
                            branch= "main",
                            output=source_output,
                            trigger=aws_codepipeline_actions.CodeCommitTrigger.POLL
                        )
                    ]
                ),
                aws_codepipeline.StageProps(
                    stage_name='Build',
                    actions=[
                        aws_codepipeline_actions.CodeBuildAction(
                            action_name='DockerBuildImage',
                            input=source_output,
                            project=props['CodeBuildDocker'],
                            run_order=1,
                        ),
                        aws_codepipeline_actions.CodeBuildAction(
                            action_name='DockerBuildImage1',
                            input=source_output,
                            project=props['CodeBuildDocker1'],
                            run_order=1,
                        )
                    ]
                )
            ]
        )

        # grant access s3 for codepipline
        props['bucket'].grant_read_write(pipeline.role)
        props['cc_repo'].grant_pull_push(pipeline.role)

        # pipeline param to get
        pipeline_param = aws_ssm.StringParameter(
            self, "PipelineParam",
            parameter_name=f"{props['projectName']}-pipeline",
            string_value=pipeline.pipeline_name,
            description='cdk pipeline bucket'
        )

        # output cfn
        CfnOutput(
            self, "piplineOut",
            description="Pipeline",
            value=pipeline.pipeline_name
        )
        
        self.output_props = props.copy()
        self.output_props['cp'] = pipeline

    # Pass object to another stack
    @property
    def outputs(self):
        return self.output_props
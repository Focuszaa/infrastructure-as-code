from aws_cdk import (
    aws_s3 as aws_s3,
    aws_ecr,
    aws_codebuild,
    aws_ssm,
    App, Aws, CfnOutput, Duration, RemovalPolicy, Stack
)


class Base(Stack):
    def __init__(self, app: App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        ArtifactBuket = aws_s3.Bucket(
            self, "artifact-bucket",
            bucket_name=f"{props['namespace'].lower()}-{Aws.ACCOUNT_ID}",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL)

        # ssm parameter to get bucket name later
        bucket_param = aws_ssm.StringParameter(
            self, "ParameterB",
            parameter_name=f"{props['namespace']}-bucket",
            string_value=ArtifactBuket.bucket_name,
            description='cdk pipeline bucket'
        )

        EcrRepo = aws_ecr.Repository(
            self, "EcrRepo",
            repository_name=f"{props['namespace']}",
            removal_policy=RemovalPolicy.DESTROY)

        # codeBuild project for running in code pipeline.
        CodeBuildDocker = aws_codebuild.PipelineProject(
            self, "codebuid-project",
            project_name=f"{props['namespace']}-Docker-build",
            build_spec=aws_codebuild.BuildSpec.from_source_filename(
                filename='buildspec.yaml'),
            environment=aws_codebuild.BuildEnvironment(
                privileged=True
            ),
            environment_variables={
                'ecr': aws_codebuild.BuildEnvironmentVariable(
                    value=EcrRepo.repository_uri
                ),
                'tag': aws_codebuild.BuildEnvironmentVariable(
                    value='cdk'
                )
            },
            description="build image",
            timeout=Duration.minutes(10),
        )

        # CodeBuild IAM Permission for s3
        ArtifactBuket.grant_read_write(CodeBuildDocker)

        # CodeBuild IAM Permission for ECR
        EcrRepo.grant_pull_push(CodeBuildDocker)

        CfnOutput(
            self, "ECR",
            description="ECR Repo",
            value=EcrRepo.repository_uri
        )
        CfnOutput(
            self, "s3Bucket",
            description="s3 bucket",
            value=ArtifactBuket.bucket_name
        )

        self.output_props = props.copy()
        self.output_props['bucket'] = ArtifactBuket
        self.output_props['CodeBuildDocker'] = CodeBuildDocker

    # Pass object to another stack
    @property
    def outputs(self):
        return self.output_props

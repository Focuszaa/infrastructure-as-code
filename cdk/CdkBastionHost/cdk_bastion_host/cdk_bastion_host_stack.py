from aws_cdk import (
    Stack,
    aws_ec2,
)
from constructs import Construct

class CdkBastionHostStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = aws_ec2.Vpc.from_lookup(
          self,"lookup-vpc",
          is_default=True
        )
        
        aws_ec2.BastionHostLinux(
          self,'CdkBastionHost',
          instance_name="CdkBastionHost",
          instance_type=aws_ec2.InstanceType.of(aws_ec2.InstanceClass.T3, aws_ec2.InstanceSize.MICRO),
          vpc=vpc,
          
        )
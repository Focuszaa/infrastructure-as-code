from aws_cdk import (
    Stack,
    aws_ec2,
)
from constructs import Construct

class CdkBastionHostStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        YOUR_VPC_ID="VPV ID"
        SUBNET="Your subnet id"
        SECURITY_GROUP_NAME="sg-bastion"
        
        vpc = aws_ec2.Vpc.from_lookup(
          self,"lookup-vpc",
          is_default=True,
          vpc_id=YOUR_VPC_ID
        )
        
        subnet = aws_ec2.Subnet.from_subnet_id(
          self, id = "subnet",
          subnet_id= SUBNET
        )
        
        sg = aws_ec2.SecurityGroup(
          self, 'sg-bastion-host',
          vpc=vpc,
          allow_all_outbound=True,
          security_group_name=SECURITY_GROUP_NAME
        )
        
        aws_ec2.BastionHostLinux(
          self,'CdkBastionHost',
          instance_name="CdkBastionHost",
          instance_type=aws_ec2.InstanceType.of(aws_ec2.InstanceClass.T3, aws_ec2.InstanceSize.MICRO),
          vpc=vpc,
          subnet_selection= subnet,
          security_group=sg,
        )
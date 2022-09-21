from aws_cdk import (
    # aws_cloudwatch as cw,
    aws_events as ev,
    aws_codecommit as cc,
    aws_iam as iam,
    aws_events_targets as targets,
    App, Aws, CfnOutput, Duration, RemovalPolicy, Stack
)

class EventTrigger(Stack):
    def __init__(self, app: App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)
        
        cw_event_service_role = iam.Role(self, "Role",
            assumed_by=iam.ServicePrincipal("events.amazonaws.com"),
            description="Event-service-role",
            inline_policies={
                'StartExecuteCodepipeline': iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=['codepipeline:StartPipelineExecution'],
                            resources=[props['cp'].pipeline_arn]
                        )
                    ]
                )
            }
        )
        
        # cc means codecommit
        cc_change_rule =ev.Rule(self, "cc_change_rule",
            event_pattern=ev.EventPattern(
              source=["aws.codecommit"],
              detail_type=['CodeCommit Repository State Change'],
              resources=[props['cc_repo'].repository_arn],
              detail={
                "event": ["referenceCreated","referenceUpdated"],
                "referenceType": "branch",
                "referenceName": "main"
              }
            )
        )
        
        cc_change_rule.add_target(targets.CodePipeline(
          props['cp'],
          event_role=cw_event_service_role,
          retry_attempts=2
        ))
        
        # cw means codewatch
        cw_schedule_weekly_rule =ev.Rule(
          self, "cw_schedule_weekly_rule",
          rule_name='WeeklyEventSchedule',
          description='Build once a week on Monday random time ~ 8-10 AM',
          schedule=ev.Schedule.expression("cron(0 1-5 ? * MON *)")
        )
        
        cw_schedule_weekly_rule.add_target(targets.CodePipeline(
          props['cp'],
          event_role=cw_event_service_role,
          retry_attempts=2
        ))

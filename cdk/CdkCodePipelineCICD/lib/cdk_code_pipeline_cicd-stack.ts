import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Bucket } from 'aws-cdk-lib/aws-s3';
import { CodePipeline, CodePipelineSource, ShellStep } from 'aws-cdk-lib/pipelines';
import { MyPipelineAppStage } from './pipeline-app-stage';
import { ManualApprovalStep } from 'aws-cdk-lib/pipelines';


export class CdkCodePipelineCicdStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const bucket = Bucket.fromBucketArn(this, 'getBucket', 'arn:aws:s3:::sorcecode')

    const pipeline = new CodePipeline(this, 'Pipeline', {
      pipelineName: 'MyPipeline',
      synth: new ShellStep('Synth', {
        input: CodePipelineSource.s3(bucket, 'sourcecode/code.zip'),
        commands: ['npm ci', 'npm run build', 'npx cdk synth']
      })
    });

    const testingStage = pipeline.addStage(new MyPipelineAppStage(this, 'testing', {
      env: { account: '1234567890', region: 'us-east-1' },
    }));

    testingStage.addPost(new ManualApprovalStep('approval'));
  }
}

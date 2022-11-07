import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Function, InlineCode, Runtime, Code } from 'aws-cdk-lib/aws-lambda';

export class MyLambdaStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
      super(scope, id, props);
  
      new Function(this, 'LambdaFunction', {
        runtime: Runtime.NODEJS_16_X,
        handler: 'index.handler',
        code: Code.fromAsset(('lambda-handler')),
      });
    }
}
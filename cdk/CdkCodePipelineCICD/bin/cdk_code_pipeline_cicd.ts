#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { CdkCodePipelineCicdStack } from '../lib/cdk_code_pipeline_cicd-stack';

const app = new cdk.App();
new CdkCodePipelineCicdStack(app, 'CdkCodePipelineCicdStack', {

  env: { account: '1234567890', region: 'us-east-1' },

});
import boto3
import os
import botocore
import argparse

def init():
    _parser = argparse.ArgumentParser(description='Husky-Not-Husky App.', epilog='More information — https://slidescript.dev')
    _parser.add_argument('--arn', help='Amazon Rekognition Custom Labels ARN', required=True)
    _parser.add_argument('--action', help='start (To start a model) |  stop (To stop a model) | identify (To identify image(s))', required=True)
    _parser.add_argument('--s3-bucket', help='')
    _parser.add_argument('--s3-path', help='')

    args = _parser.parse_args()
    if not args.arn:
        raise ValueError('Amazon Rekognition Custom Labels Model ARN isn\'t detected')

    if args.action=='start':
        start_project(args.arn)
    elif args.action=='stop':
        stop_project(args.arn)
    elif args.action=='identify':
        identify(args.arn, args.s3_bucket, args.s3_path)



def start_project(arn):                
    try:
        print('Starting model.')
        _rekognition = boto3.client('rekognition', region_name='us-east-1')
        response = _rekognition.start_project_version(
            ProjectVersionArn=arn,
            MinInferenceUnits=1
        )    
        print('Model is started.')
    except _rekognition.exceptions.ResourceInUseException:
        print('Model is already running.')

def stop_project(arn):
    try:
        print('Stopping model.')
        _rekognition = boto3.client('rekognition', region_name='us-east-1')
        response = _rekognition.stop_project_version(
            ProjectVersionArn=arn
        )
        print('Model is stopping.')
    except _rekognition.exceptions.ResourceInUseException:
        print('Model is already stopped.')


def identify(arn, s3_bucket, s3_path):
    _rekognition = boto3.client('rekognition', region_name='us-east-1')
    response = _rekognition.detect_custom_labels(
        ProjectVersionArn=arn,
        Image={
            'S3Object': {
                'Bucket': s3_bucket,
                'Name': s3_path
            }
        },
    )
    if response:
        if 'CustomLabels' in response:
            for label in response['CustomLabels']:
                print('{} detected as {} with confidence level {}'.format(s3_path, label['Name'], label['Confidence']))

if __name__ == '__main__':
    init()
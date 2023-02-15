import json
import boto3
import base64

def lambda_handler(event, context):
    bucket_name = 'test'
    source_key = 'test-1.jpeg'
    target_key = 'target.png'

    base_64ed_image = event['body']
    print(event['queryStringParameters'])
    if event['queryStringParameters']['target_image'] == '2':
        source_key = 'test-2.png'
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.put_object(
                    Key=target_key,
                    Body=base64.b64decode(base_64ed_image.encode("UTF-8")),
                    ContentType='image/png')
    rekognition = boto3.client('rekognition')
    response = rekognition.compare_faces(
        SourceImage={'S3Object':{'Bucket': bucket_name, 'Name': source_key}},
        TargetImage={'S3Object':{'Bucket': bucket_name, 'Name': target_key}}
    )
    return {
            'statusCode': 200,
            'body': response
    }
    

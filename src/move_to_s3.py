import boto3
import os

def print_s3_contents_boto3(connection):
    for bucket in connection.buckets.all():
        for key in bucket.objects.all():
            print(key.key)

if __name__ == '__main__':
    boto3_connection = boto3.resource('s3')
    s3_client = boto3.client('s3')
    bucket_name = 'user_reviews-bucket'
    boto3_connection.create_bucket(Bucket=bucket_name)
    for f in os.path.join("..","data","reviews"):
        s3_client.upload_file(f, bucket_name, f)
    print_s3_contents_boto3(boto3_connection)

import boto3
from os import listdir
from os.path import isfile, join

def print_s3_contents_boto3(connection):
    for bucket in connection.buckets.all():
        for key in bucket.objects.all():
            print(key.key)

if __name__ == '__main__':
    boto3_connection = boto3.resource('s3')
    s3_client = boto3.client('s3')
    bucket_name = 'user-reviews-bucket'
    boto3_connection.create_bucket(Bucket=bucket_name)
    reviews_dir = '../data/reviews/'
    files = [f for f in listdir(reviews_dir) if isfile(join(reviews_dir,f))]
    file_paths = [reviews_dir + f for f in listdir(reviews_dir) if isfile(join(reviews_dir,f))]
    for i,path in enumerate(file_paths):
        print(path)
        s3_client.upload_file(path, bucket_name, files[i])
    print_s3_contents_boto3(boto3_connection)

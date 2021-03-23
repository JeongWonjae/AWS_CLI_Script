import boto3
import json

session=boto3.session.Session(profile_name='DemoUser', region_name='us-east-1')
client=session.client('s3')

# for minimize call API set 'MaxResults=1000'
response=client.list_buckets()
# response = {'ResponseMetadata': {'RequestId': '2MZKR0N2WGKK3EEV', 'HostId': '87QXu4DfD/e2DavOXqCIwZIBCnWy03twI2vxX/EhK

bucket_names=[]
for bucket in response['Buckets']:
    bucket_names.append(bucket['Name'])

with open('./s3-bucket.json', 'w+') as f:
    json.dump(bucket_names, f, indent=4, default=str)
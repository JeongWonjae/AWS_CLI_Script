import boto3

session=boto3.session.Session(profile_name='DemoUser', region_name='us-east-1')
client=session.client('s3')

response=client.list_buckets()
# response = {'ResponseMetadata': {'RequestId': '2MZKR0N2WGKK3EEV', 'HostId': '87QXu4DfD/e2DavOXqCIwZIBCnWy03twI2vxX/EhK

bucket_names=[]
for bucket in response['Buckets']:
    bucket_names.append(bucket['Name'])
# bucket_names = {'bucket1', 'bucket2' ... }

bucket_objects={}

for bck in bucket_names:
    # if not exists object, return to 'none'
    response=client.list_objects_v2(Bucket=bck, MaxKeys=1000)

    if response.get('Contents'):
        bucket_objects[bck]=response['Contents']
    else:
        bucket_objects[bck]=[]
        continue

    # start recursive
    while response['IsTruncated']:
        response=client.list_objects_v2(Bucket=bck, MaxKeys=1000, ContinuationToken=response['NextContinuationToken'])
        bucket_objects[bck].extend(response['Contents'])

# print (s3 bucket-objects)
for bck in bucket_names:
    with open('./{}.txt'.format(bck), 'w+') as f:
        for bucket_object in bucket_objects[bck]:
            f.write('{} ({} bytes)\n'.format(bucket_object['Key'],bucket_object['Size']))

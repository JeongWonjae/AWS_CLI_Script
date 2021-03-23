import boto3
import json

session=boto3.session.Session(profile_name='DemoUser', region_name='us-east-1')
client=session.client('ec2')

instances=[]
# for minimize call API set 'MaxResults=1000'
response=client.describe_instances(MaxResults=1000)
# response = {'Reservations': [{'Groups': [], 'Instances': [{'AmiLaunchIndex': 0, 'ImageId': 'ami-0533f2ba8a1995cf9', 'InstanceId': 'i-09bbe296b89xxxxx', 'InstanceType': 't2.micro', 'KeyName': 'EC2DemoKey', 'LaunchTime': datetime.datetime(2021, 3, 23, 14, 28, 8, tzinfo=tzutc()), 'Monitoring': {'State': 'disabled'}, 'Placement': {'AvailabilityZone': 'us-east-1a', 'GroupName': '', 'Tenancy': 'default'}, 'PrivateDnsName': 'ip-172-31-1-111.ec2.internal', 'PrivateIpAddress': '172.31.1.111', 'ProductCodes': [], 'PublicDnsName': '', 'State': {'Code': 16, 'Name': 'running'}, 'StateTransitionReason': '', 'SubnetId': 'subnet-0245c04d58e1998d3', 'VpcId': 'vpc-4f65d132', 'Architecture': 'x86_64', 'BlockDeviceMappings': [{'DeviceName': '/dev/xvda', 'Ebs': {'AttachTime': datetime.datetime(2021, 3, 23, 14, 28, 9, tzinfo=tzutc()), 'DeleteOnTermination': True, 'Status': 'attached', 'VolumeId': 'vol-0d4dcaf9ea658bf8e'}}], 'ClientToken': '', 'EbsOptimized': False, 'EnaSupport': True, 'Hypervisor': 'xen', 'NetworkInterfaces': [{'Attachment': {'AttachTime': datetime.datetime(2021, 3, 23, 14, 28, 8, tzinfo=tzutc()), 'AttachmentId': 'eni-attach-04ef9e8fe41f0b730', 'DeleteOnTermination': True, 'DeviceIndex': 0, 'Status': 'attached', 'NetworkCardIndex': 0}, 'Description': 'Primary network interface', 'Groups': [{'GroupName': 'launch-wizard-1', 'GroupId': 'sg-028e98f8644954d4f'}], 'Ipv6Addresses': [], 'MacAddress': '12:f7:a1:50:f6:3f', 'NetworkInterfaceId': 'eni-0989b13d333faecaa', 'OwnerId': '416168070872', 'PrivateDnsName': 'ip-172-31-1-111.ec2.internal', 'PrivateIpAddress': '172.31.1.111', 'PrivateIpAddresses': [{'Primary': True, 'PrivateDnsName': 'ip-172-31-1-111.ec2.internal', 'PrivateIpAddress': '172.31.1.111'}], 'SourceDestCheck': True, 'Status': 'in-use', 'SubnetId': 'subnet-0245c04d58e1998d3', 'VpcId': 'vpc-4f65d132', 'InterfaceType': 'interface'}], 'RootDeviceName': '/dev/xvda', 'RootDeviceType': 'ebs', 'SecurityGroups': [{'GroupName': 'launch-wizard-1', 'GroupId': 'sg-028e98f8644954d4f'}], 'SourceDestCheck': True, 'VirtualizationType': 'hvm', 'CpuOptions': {'CoreCount': 1, 'ThreadsPerCore': 1}, 'CapacityReservationSpecification': {'CapacityReservationPreference': 'open'}, 'HibernationOptions': {'Configured': False}, 'MetadataOptions': {'State': 'applied', 'HttpTokens': 'optional', 'HttpPutResponseHopLimit': 1, 'HttpEndpoint': 'enabled'}, 'EnclaveOptions': {'Enabled': False}}], 'OwnerId': '416168070872', 'ReservationId': 'r-057f164d12660c27d'}], 'ResponseMetadata': {'RequestId': 'f136cfd9-fe0b-4b87-b0de-b9d755045070', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'f136cfd9-fe0b-4b87-b0de-b9d755045070', 'cache-control': 'no-cache, no-store', 'strict-transport-security': 'max-age=31536000; includeSubDomains', 'content-type': 'text/xml;charset=UTF-8', 'content-length': '6267', 'vary': 'accept-encoding', 'date': 'Tue, 23 Mar 2021 14:31:47 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}

# get information of instance up to 1000
for rev in response['Reservations']:
    if rev.get('Instances'):
        instances.extend(rev['Instances'])

# if ec2 instances are over 1000
while response.get('NextToken'):
    response=client.describe_instances(MaxResults=1000, NextToken=response['NextToken'])
    for rev in response['Reservations']:
        if rev.get('Instances'):
            instances.extend(rev['Instances'])

with open('./ec2-instances.json', 'w+') as f:
    json.dump(instances, f, indent=4, default=str)
import boto3
import json

session=boto3.session.Session(profile_name="DemoUser", region_name="useast-1")

client=session.client("iam")

user_list=[]
group_list=[]
role_list=[]
policy_list=[]

# Require about IAM Access Policy to session
response=client.get_account_authorization_details()

if response.get('UserDetailList'):
    user_list.extend(response['UserDetailList'])
if response.get('GroupDetailList'):
    group_list.extend(response['GroupDetailList'])
if response.get('RoleDetailList'):
    role_list.extend(response['RoleDetailList'])
if response.get('Policies'):
    group_list.extend(response['Policies'])

# IAM result is pagination
while response['IsTruncated']:
    response=client.get_account_authorization_details(Marker=response['Marker'])
    if response.get('UserDetailList'):
        user_list.extend(response['UserDetailList'])
    if response.get('GroupDetailList'):
        group_list.extend(response['GroupDetailList'])
    if response.get('RoleDetailList'):
        role_list.extend(response['RoleDetailList'])
    if response.get('Policies'):
        group_list.extend(response['Policies'])

with open('./users.json', 'w+') as f:
    json.dump(user_list, f, indent=4, default=str)
with open('./group.json', 'w+') as f:
    json.dump(group_list, f, indent=4, default=str)
with open('./roles.json', 'w+') as f:
    json.dump(role_list, f, indent=4, default=str)
with open('./policies.json', 'w+') as f:
    json.dump(policy_list, f, indent=4, default=str)
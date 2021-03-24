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

'''
# Require about IAM Access Policy to session
# Return to user name
currentUser=client.get_user()['User']
'''
userName=client.get_user()['User']['UserName']

for usr in user_list:
    if usr['UserName']==userName:
        currentUser=usr
        break

inlinePolicies=[]
managedPolicies=[]

# Get Inline policy
if currentUser.get('UserPolicyList'):
    for policy in currentUser['UserPolicyList']:
        inlinePolicies.append(policy['PolicyDocument'])

# Get management policy
if currentUser.get('AttachedManagedPolicies'):
    for managedPolicy in currentUser['AttachedManagedPolicies']:
        policyName=managedPolicy['PolicyName']
        managedPolicies.append(policyName)
        '''
        if managedPolicy['PolicyArn']:
            print('point1')
            policyARN=managedPolicy['PolicyArn']
            for poi in policy_list:
                if policy_list['Arn']==policyARN:
                    defaultVersion=poi['DefaultVersionId']
                    for ver in poi['PolicyVersionList']:
                        if ver['VersionId']==defaultVersion:
                            managedPolicies.append(ver['Document'])

                    break
            break
        '''
with open('./currentUserPolicies.json', 'w+') as f:
    json.dump(managedPolicies, f, indent=4, default=str)
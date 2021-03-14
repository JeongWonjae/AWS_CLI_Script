import os
import json
import time
import re
startTime=time.time()
resourceTotalCount=0
# Get CMD
os.system('cd {}'.format(os.getcwd()))

# Define resource type
# Need to append type name
resourceType=['AWS::KMS::Key','AWS::EC2::Instance','AWS::S3::Bucket']

# Get certain resource's id
for rscType in resourceType:
    command="aws configservice list-discovered-resources --resource-type \"{}\"".format(rscType)
    output=os.popen(command).read()
    getJsonData=json.loads(output)
    # result=> getJsonData = {'resourceIdentifiers': [{'resourceType': 'AWS::EC2::Instance', 'resourceId': 'i-03598a6854ad4e59e'}]}

    resourceIdList=[]
    resourceCount=len(getJsonData['resourceIdentifiers'])
    # Print resource type & resources Id
    print("=========",rscType,"==========")
    print("Find {} resources".format(resourceCount))
    resourceTotalCount+=resourceCount

    # IF there's not resource,
    if resourceCount==0:
        continue
    # IF there's only one resource,
    elif resourceCount==1:
        id=getJsonData['resourceIdentifiers'][0]['resourceId']
        # result=> id=subnet-db7610fa
        resourceIdList.append(id)
    # If there's more than two resources,
    else:
        for idx in range(0, resourceCount-1):
            id=getJsonData['resourceIdentifiers'][idx]['resourceId']
            # result=> id=subnet-db7610fa
            resourceIdList.append(id)

    # Get resource's config content
    command="aws configservice get-resource-config-history --resource-type {} --resource-id ".format(rscType)
    for id in resourceIdList:
        resourceConfig=os.popen(command+id).read()
        print('-----------------------------')
        print(resourceConfig)


endTime=time.time()
print("\n\nTotal resource count: {}".format(resourceTotalCount))
print("Working time: {} sec".format(endTime-startTime))
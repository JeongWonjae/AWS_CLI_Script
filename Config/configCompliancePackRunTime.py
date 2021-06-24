import os
import json
import time

compliancePackName="CustomCompliancePack"
compliancePackS3URI="s3://demos3bucket-wj/compliancePack/configCustomCompliancePack.yaml"
countAPICall=0

startTime=time.time()

# Get CMD
os.system('cd {}'.format(os.getcwd()))

# Deploy Compliance Pack
print("[+]Deploy Compliance Pack")
command = "aws configservice put-conformance-pack --conformance-pack-name {} --template-s3-uri {}".format(compliancePackName, compliancePackS3URI)
output = os.popen(command).read()
countAPICall+=1

# Waiting Compliance Pack Deploy Completed
time.sleep(5)
while True:
    command = "aws configservice describe-conformance-pack-status --conformance-pack-names {}".format(compliancePackName)
    countAPICall += 1
    output = os.popen(command).read()
    getJsonData = json.loads(output)
    deployStatus = getJsonData['ConformancePackStatusDetails'][0]['ConformancePackState']
    if deployStatus=="CREATE_COMPLETE":
        deployPackStartTime=getJsonData['ConformancePackStatusDetails'][0]['LastUpdateRequestedTime']
        deployPackEndTime=getJsonData['ConformancePackStatusDetails'][0]['LastUpdateCompletedTime']
        break
    else:
        time.sleep(2)
        continue

# Evaluation Compliance
while True:
    command = "aws configservice get-conformance-pack-compliance-summary --conformance-pack-names {}".format(compliancePackName)
    countAPICall+=1
    output=os.popen(command).read()
    getJsonData=json.loads(output)
    evalStatus=getJsonData['ConformancePackComplianceSummaryList'][0]['ConformancePackComplianceStatus']
    if evalStatus=="NON_COMPLIANT" or evalStatus=="COMPLIANT":
        break
    elif evalStatus=="INSUFFICIENT_DATA":
        time.sleep(5)
        continue
    else:
        continue

endTime=time.time()
print("[+]Compliance Pack Deploy Start time: {}".format(deployPackStartTime))
print("[+]Compliance Pack Deploy End time: {}".format(deployPackEndTime))
print("[+]Total API Call Count: {}".format(countAPICall))
print("[+]Total Working time: {} sec".format(endTime-startTime))
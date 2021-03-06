import boto3
from shared.common import * 

class LAMBDA(object):
    
    def __init__(self, vpc_id, region_name):
        self.vpc_id = vpc_id
        self.region_name = region_name
    
    def run(self):
        try:
            client = boto3.client('lambda',region_name=self.region_name)
            
            response = client.list_functions()
            
            message_handler("\nChecking LAMBDA FUNCTIONS...", "HEADER")

            if (len(response["Functions"]) == 0):
                message_handler("Found 0 Lambda Functions in region {0}".format(self.region_name), "OKBLUE")
            else:
                found = 0
                message = ""
                for data in response["Functions"]:
                    if (data['VpcConfig']['VpcId'] == self.vpc_id):
                        found += 1
                        message = message + "\nFunctionName: {0} - Runtime: {1} - VpcId {2} - SubnetIds: {3}".format(
                            data["FunctionName"], 
                            data["Runtime"], 
                            data['VpcConfig']['VpcId'], 
                            ", ".join(data['VpcConfig']['SubnetIds'])
                        )
                message_handler("Found {0} Lambda Functions using VPC {1} {2}".format(str(found), self.vpc_id, message),'OKBLUE')
                

        except Exception as e:
            message = "Can't list Lambda Functions\nError {0}".format(str(e))
            exit_critical(message)

class EC2(object):

    def __init__(self, vpc_id, region_name):
        self.vpc_id = vpc_id
        self.region_name = region_name
    
    def run(self):
        try:
            
            client = boto3.client('ec2',region_name=self.region_name)

            response = client.describe_instances()
            
            message_handler("\nChecking EC2 Instances...", "HEADER")

            if (len(response["Reservations"]) == 0):
                message_handler("Found 0 EC2 Instances in region {0}".format(self.region_name), "OKBLUE")
            else:
                found = 0
                message = ""
                for data in response["Reservations"]:
                    for instances in data['Instances']:
                        if "VpcId" in instances:
                            if (instances['VpcId'] == self.vpc_id):
                                found += 1
                                message = message + "\nInstanceId: {0} - PrivateIpAddress: {1} - VpcId {2} - SubnetIds: {3}".format(
                                    instances["InstanceId"], 
                                    instances["PrivateIpAddress"], 
                                    instances['VpcId'], 
                                    instances['SubnetId']
                                )
                message_handler("Found {0} EC2 Instances using VPC {1} {2}".format(str(found), self.vpc_id, message),'OKBLUE')

        except Exception as e:
            message = "Can't list EC2 Instances\nError {0}".format(str(e))
            exit_critical(message)

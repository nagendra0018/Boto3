import boto3


AWS_REGION = "us-east-1"
AMI_ID = "ami-08f44e8eca9095668"
INSTANCE_TYPE = "t2.medium"
KEY_PAIR_NAME = "nag-in"
SECURITY_GROUP_ID = "sg-07341526e9e2540b3"
SUBNET_ID = "subnet-0cd8d94cc14984f8b"
SERVER_NAME = "boto3-server"


def validate_network(ec2):
	subnet = ec2.describe_subnets(SubnetIds=[SUBNET_ID])["Subnets"][0]
	security_group = ec2.describe_security_groups(GroupIds=[SECURITY_GROUP_ID])["SecurityGroups"][0]

	if subnet["VpcId"] != security_group["VpcId"]:
		raise ValueError(
			"Security group and subnet must be in the same VPC. "
			f"Subnet {SUBNET_ID} is in {subnet['VpcId']}; "
			f"security group {SECURITY_GROUP_ID} is in {security_group['VpcId']}."
		)


def create_server():
	ec2 = boto3.client("ec2", region_name=AWS_REGION)
	validate_network(ec2)

	response = ec2.run_instances(
		ImageId=AMI_ID,
		InstanceType=INSTANCE_TYPE,
		KeyName=KEY_PAIR_NAME,
		SecurityGroupIds=[SECURITY_GROUP_ID],
		SubnetId=SUBNET_ID,
		MinCount=1,
		MaxCount=1,
		TagSpecifications=[
			{
				"ResourceType": "instance",
				"Tags": [
					{"Key": "Name", "Value": SERVER_NAME}
				],
			}
		],
	)

	instance = response["Instances"][0]
	instance_id = instance["InstanceId"]
	print(f"Created EC2 instance: {instance_id}")
	return instance_id


if __name__ == "__main__":
	create_server()

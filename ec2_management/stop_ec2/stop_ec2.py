import boto3


# List instances if you want to run specific instances
instances = []

# AWS region
region = 'eu-west-1'

# AWS service
ec2 = boto3.client('ec2', region_name=region)

# Get all instances id
all_instances = [instance.id for instance in ec2.instances.all()]

def lambda_handler(event, context):
    if instances == 0:
        ec2.stop_instances(InstanceIds=instances)
    else:
        ec2.stop_instances(InstanceIds=all_instances)

    print('stopped your instances: ' + str(instances))
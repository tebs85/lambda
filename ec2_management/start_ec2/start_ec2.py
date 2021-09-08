import boto3


# List instances if you want to run specific instances
instances = []

# AWS region
region = 'eu-west-1'

# AWS service
ec2 = boto3.client('ec2', region_name=region)

# Get all instances id
def get_all_instanes_id():
    
    all_instances = []
    
    describe_instances = ec2.describe_instances()
    
    for instances in describe_instances['Reservations']:
        for instance in instances['Instances']:
            all_instances.append(instance['InstanceId'])
        
    return all_instances

def lambda_handler(event, context):
    if instances == 0:
        ec2.stop_instances(InstanceIds=instances)
        print('started your instances: ' + str(instances))
    else:
        ec2.stop_instances(InstanceIds=get_all_instanes_id())
        print('started your instances: ' + str(get_all_instanes_id()))
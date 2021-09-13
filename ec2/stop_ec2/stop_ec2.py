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

# Get all instances tags (auto start/stop)
def get_all_instanes_by_tag():
    
    all_instances = []
    
    describe_instances = ec2.describe_instances()
    
    for instances in describe_instances['Reservations']:
        for instance in instances['Instances']:
            for tag in instance['Tags']:
                if tag['Key'] == "autoManageInstanceSatus":
                    if tag['Value'] == 'started':
                        all_instances.append(instance['InstanceId'])
        
    return all_instances
    
def lambda_handler(event, context):

    if instances == 0:
        all_instanes_by_tag = get_all_instanes_by_tag()
        ec2.stop_instances(InstanceIds=all_instanes_by_tag)
        ec2.create_tags(Resources=all_instanes_by_tag, Tags=[{'Key': 'autoManageInstanceSatus', 'Value': 'stopped'}])
        print('started your instances: ' + str(all_instanes_by_tag))
    elif get_all_instanes_by_tag() == 0: 
        all_instanes_id = get_all_instanes_id()
        ec2.stop_instances(InstanceIds=all_instanes_id)
        print('started your instances: ' + str(all_instanes_id))
    else:
        ec2.stop_instances(InstanceIds=instances)
        print('started your instances: ' + str(instances))


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
                # print(tag['Key'] == "autoManageInstanceSatus")
                if tag['Key'] == "autoManageInstanceSatus":
                    if tag['Value'] == 'start':
                        all_instances.append(instance['InstanceId'])
        
    return all_instances
    
def lambda_handler(event, context):

    if instances == 0:
        ec2.start_instances(InstanceIds=get_all_instanes_by_tag())
        print('started your instances: ' + str(get_all_instanes_by_tag()))
    elif get_all_instanes_by_tag() == 0: 
        ec2.start_instances(InstanceIds=get_all_instanes_id())
        print('started your instances: ' + str(get_all_instanes_id()))
    else:
        ec2.start_instances(InstanceIds=instances)
        print('started your instances: ' + str(instances))

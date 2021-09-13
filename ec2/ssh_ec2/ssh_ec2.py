import time
import boto3
import paramiko
from io import StringIO

 
# Get Parameter from SSM
# @param param - string | list comma seperated
def get_parameters(param):
    
    # Boot up SSM client
    ssm = boto3.client('ssm')
    
    # Retrieve SSM from Parameter Store
    response = ssm.get_parameters(
        Names=[param],WithDecryption=True
    )
    
    for parameter in response['Parameters']:
        return parameter['Value']
        
# Get RSA Key parameter store
privkey = paramiko.RSAKey.from_private_key(file_obj=StringIO(get_parameters('/ec2/rsakey')))

 
# Start SSH Client
ssh = paramiko.SSHClient()

 
# Attaching IAM Policy
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


# Connect to ec2 instance
# @param ip - string
# @param username - string
def connect_ssh(ip, username):
    connected = False

    try:
        ssh.connect(hostname=ip, port=22, username=username, pkey=privkey)
        connected = True
        return connected
    except:
        ssh.close()

 

# Run shell commands on ec2 instance
# @param cmd - string
def run_command(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdin.flush()
    
    data = stdout.read().splitlines()
    
    for line in data:
        print(line)
        

 

#intialize the script
def lambda_handler(event, context):

 
    ec2 = boto3.resource('ec2', region_name='eu-west-1')
    
    # Add array with options
    # [instance_id, ip, username, command]
    instances = [
        ['i-0123a4bc5de6f89g0', '10.0.0.1', 'oracle',  [ "whoami", "ls -l"] ], 
        ['i-0123a4bc5de6f89g0', '10.0.0.1', 'ec2-user',  [ "whoami", "ls -lah"] ]
    ]
    
    for instance in instances:

        instance_id = instance[0]
        ip = instance[1]
        username = instance[2]
        commandArray =instance[3]
        instance = ec2.Instance(instance_id)
        
        print("=================================================")
        print("Instance - ", instance)
        print('=================================================')

 
        isConnected = connect_ssh(ip, username)
        
        if (isConnected) :
            commands = commandArray
            
            for cmd in commands:
                run_command(cmd)
    
            ssh.close()    
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import time
import boto3
import paramiko
from io import StringIO

 
# Get Parameter from SSM
# @param - string | list comma seperated
def get_parameters(param):
    
    # Boot up SSM client
    ssm = boto3.client('ssm')
    
    # Retrieve SSM from Parameter Store
    response = ssm.get_parameters(
        Names=[param],WithDecryption=True
    )
    
    for parameter in response['Parameters']:
        return parameter['Value']

def set_parameters(param):
    
    # Boot up SSM client
    ssm = boto3.client('ssm')
    
    # Retrieve SSM from Parameter Store
    response = ssm.set_parameters(
        Names=[param],WithDecryption=True
    )
    
    for parameter in response['Parameters']:
        return parameter['Value']

region ='eu-west-1'

# Get RSA Key parameter store
privkey = paramiko.RSAKey.from_private_key(file_obj=StringIO(get_parameters('/ec2/rsakey')))

 
# Start SSH Client
ssh = paramiko.SSHClient()

 
# Attaching IAM Policy
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


# Connect to ec2 instance
# @ip - string
# @username - string
def connect_ssh(ip, username):
    connected = False

    try:
        ssh.connect(hostname=ip, port=22, username=username, pkey=privkey)
        connected = True
        return connected
    except:
        ssh.close()

 

# Run shell commands on ec2 instance
# @cmd - string
def run_command(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdin.flush()
    
    data = stdout.read().splitlines()
    
    for line in data:
        print(line)
        
def generate_key_pair(comment):
    key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=2048)
    private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.TraditionalOpenSSL,
            crypto_serialization.NoEncryption())
    public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH)

    private_key_str = private_key.decode('utf-8')
    public_key_str = public_key.decode('utf-8') + " " + comment

    return [private_key_str, public_key_str]


def upload_keys_s3(public_key, bucket, filename):
    s3 = boto3.client('s3')
    s3.put_object(Body=public_key, Bucket=bucket, Key=filename) 

# Intialize the script
def lambda_handler(event, context):

    ec2 = boto3.resource('ec2', region_name=region)
    
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
        
        print("=" * 60)
        print("Instance: ", instance)
        print("=" * 60)

 
        isConnected = connect_ssh(ip, username)
        
        if (isConnected) :
            commands = commandArray
            
            for cmd in commands:
                run_command(cmd)
    
            ssh.close()    
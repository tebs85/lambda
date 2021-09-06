# AWS Lamda function to manage EC2

This project is documenting Lamda functions, I'm using to manage the AWS EC2 instances. The scripts are solving various issues for teams in managing workloads on AWS. 
I will be using various languages (Python, Typescript) to write the functions and most of the functions are being used in production workloads. Feel free to use them in your projects.


## Prerequisites

* AWS account
* Python
* Typescript
* Docker


## Repo structure

1. Source folder: cdk app written in TypeScript

2. Root folder:
    * `ec2_management` Automate SysAdmin functions
    * `rds_management` Automate DBA functions
    * `security`       Automate security testing and alerting
    

## Getting started (AWS)

1. Go to the `module` and inside you will find lambda folder for various functions

2. Select the `function` you need to utilise like `ssh_ec2`

3. Inside the is a main lamda file and requirements.txt for additional packages

4. Add the required packages

5. Zip file and upload to AWS 



## Getting started (Local)

You can deploy your Lambda function code as a container image. AWS provides the following resources to help you build a container image for your Python function:

[AWS Documentation available here](https://docs.aws.amazon.com/lambda/latest/dg/python-image.html)



 ## Submitting an issue

 If you encounter a bug in the code, please first search the list of current open Issues on the GitHub repository. You may add additional feedback on an existing bug report. If the issue you're having has not yet been reported, please open a new issue. There is a template available for new issues. Please fill out all information requested in the template so we can help you more easily.

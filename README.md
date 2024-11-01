# Artifactory server Cloudformation+Python deployment

![Amazon Web Services Badge](https://img.shields.io/badge/Amazon%20Web%20Services-232F3E?logo=amazonwebservices&logoColor=fff&style=for-the-badge)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Amazon EC2 Badge](https://img.shields.io/badge/Amazon%20EC2-F90?logo=amazonec2&logoColor=fff&style=for-the-badge)
![Amazon Identity Access Management Badge](https://img.shields.io/badge/Amazon%20Identity%20Access%20Management-DD344C?logo=amazoniam&logoColor=fff&style=for-the-badge)
![Ubuntu Badge](https://img.shields.io/badge/Ubuntu-E95420?logo=ubuntu&logoColor=fff&style=for-the-badge)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![YAML](https://img.shields.io/badge/yaml-%23ffffff.svg?style=for-the-badge&logo=yaml&logoColor=151515)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939.svg?style=for-the-badge&logo=Jenkins&logoColor=white)
![Groovy](https://img.shields.io/badge/Apache%20Groovy-4298B8.svg?style=for-the-badge&logo=Apache-Groovy&logoColor=white)

This document provides steps for securely performing the deployment of an Artifactory server via CloudFormation automated with Jenkins and Python.
It also explains how to manage the AWS credentials in a Jenkins pipeline to create an AWS session and send as params to the Python deployment script.

## Prerequisites
- Jenkins installed and configured.
- Jenkins Credentials Plugin installed.
- AWS CLI and boto3 Python library installed on the Jenkins agent (or installed via the pipeline).
- AWS environment have a IAM role created for jenkins, called "jenkins-role" that the jenkins agent/script can perform assume role operation.
- The file deploy_helper/aws_accounts contain the proper account IDs and regions for each deployment environment (AWS Account).
- the AWS environment has a proper VPC deployed with:
    - 2 ELB Subnets
    - AMI for the EC2 instance
    - A key to access the instance
    - A subnet for the instance


### Alternative for Jenkins access to AWS
Alternative: Using IAM Roles for Jenkins on AWS
If your Jenkins instance is running on an AWS environment (e.g., EC2 or ECS), you can assign an IAM role to the instance or container. This approach avoids handling credentials directly.

Create an IAM Role with the necessary permissions (e.g., CloudFormationFullAccess).
Attach the IAM role to the EC2 instance or ECS task that Jenkins is running on.
Modify run.py:
Remove any arguments for aws_access_key and aws_secret_key.
The boto3 library will automatically detect and use the instance role's credentials.


## CFN Templates
The CFN file, artifactory.json, was created and manually run back in 2016.


### Artifactory Stack Parameters
The following parameters are those that were used to create the current Artifactory stack.

| Key                   | Value                 |
| :-----                | :------               |
| EC2Name	            | ENV-ARTIFACTORY       |
| ELBSubnet1	        | subnet-1234abcd       |
| ELBSubnet2	        | subnet-1234abcd       |
| InstanceAMI	        | ami-1234abcd          |
| KeyName               | acampos               |
| SubnetID	            | subnet-1234abcd       |
| VPCID	                | vpc-1234abcd          |
| ec2accesslocation     | 10.172.0.0/22         |
| ec2accesslocation2    | 192.168.55.0/24       |

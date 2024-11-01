import os
import logging
import argparse
from deploy_helper import deployment_helper as helper


def deploy_iam_stack(cfn_client, stack_root_name, environment):
    logging.info("Deploy the IAM stack")

    iam_template = helper.read_file(os.path.dirname(__file__),
                                     '..',
                                     'files',
                                     'CFN',
                                     'iam.yaml')

    stackname = f'{stack_root_name}-iam'

    iam_params = {
        'Environment': environment,
        'Stackname': stackname
    }
    
    helper.create_or_update_stack(
        cf_client=cfn_client,
        stack_name=stackname,
        template_body=iam_template,
        parameters=iam_params
    )


def deploy_artifactory_stack(cfn_client, stack_root_name, environment):
    logging.info("Deploy the ARTIFACTORY stack")
    
    artifactory_template = helper.read_file(os.path.dirname(__file__),
                                     '..',
                                     'files',
                                     'CFN',
                                     'artifactory.yaml')

    stackname = f'{stack_root_name}-ec2'

    artifactory_params = {
        'InstanceAMI': 'ami-086b16d6badeb5716',
        'KeyName': 'acampos_key',
        'VPCID': "vpc-1234abcd",
        'SubnetID': "subnet-1234abcd",
        'EC2Name': stack_root_name,
        'ec2accesslocation': '10.172.0.0/22',
        'ec2accesslocation2': '192.168.55.0/24'
    }

    helper.create_or_update_stack(
        cf_client=cfn_client,
        stack_name=stackname,
        template_body=artifactory_template,
        parameters=artifactory_params
    )


def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)

    parser = argparse.ArgumentParser()
    
    # Define expected arguments
    parser.add_argument("--environment", required=True, help="The deployment environment")
    parser.add_argument("--branch", required=True, help="The branch name")
    parser.add_argument("--region", required=True, help="The region for deployment")
    parser.add_argument("--aws-access-key", required=False, help="AWS access key ID.")
    parser.add_argument("--aws-secret-key", required=False, help="AWS secret access key.")
    parser.add_argument("--aws-session-token", required=False, help="AWS session token.")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Access the arguments as properties of `args`
    environment = args.environment
    branch = args.branch
    region = args.region
    aws_access_key = args.aws_access_key
    aws_secret_key = args.aws_secret_key
    aws_session_token = args.aws_session_token
    
    if args.environment == 'dev':
        stack_root_name = f'{branch}-artifactory'
    else:
        stack_root_name = f'{environment}-artifactory'

    aws_session = helper.get_aws_session(aws_access_key=aws_access_key, aws_secret_key=aws_secret_key, aws_session_token=aws_session_token, region=region)
    cfn_client = helper.get_cfn_client(session=aws_session)

    deploy_iam_stack(cfn_client, stack_root_name, environment)
    deploy_artifactory_stack(cfn_client, stack_root_name, environment)


if __name__ == '__main__':
    main()

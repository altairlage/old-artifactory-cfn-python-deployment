import groovy.json.JsonSlurper

def githubUser = 'jenkins-gh'
def githubServerName = ''
def repoName = 'artifactory'

def githubUrl = "https://${githubServerName}/${repoName}.git"
def branch = (env.BRANCH_NAME)
def environment = getEnvironmentFromBranch(branch)

this.getProps()

node('ubuntu_bionic') {

    // Initial cleanup
    deleteDir()

    // Main functions
    try {
        stage('Checkout') {
            dir('files') {
                println("Service code branch: ${branch}")
                checkOut(githubUrl, branch, githubUser)
            }
        }

        stage('Deploying Artifactory') {
            dir('files') {
                sts = getStsCreds(environment)
                withEnv(["AWS_ACCESS_KEY_ID=${sts[0]}", "AWS_SECRET_ACCESS_KEY=${sts[1]}", "AWS_SESSION_TOKEN=${sts[2]}"]) {
                    sh("python3 run.py --environment ${environment} --branch ${branch} --region ${region} --aws-access-key $AWS_ACCESS_KEY_ID  --aws-secret-key $AWS_SECRET_ACCESS_KEY --aws-session-token $AWS_SESSION_TOKEN")
                }
            }
        }
    } catch (e) {
        echo 'Err: Incremental Build failed with Error: ' + e.getMessage()
        throw e
    } finally {
        // This final cleanup prevents successful and
        // failed build files from sitting on the volume
        deleteDir()
    }
}


def getProps() {
    properties(
        [
            [
                $class:'ParametersDefinitionProperty',
                parameterDefinitions: [
                    [
                        $class: 'ChoiceParameterDefinition',
                        name: 'region',
                        choices: 'us-west-2\nus-east-1\neu-central-1\neu-west-1\nap-northeast-1',
                        description: 'Environment account region',
                        defaultValue: 'us-west-2'
                    ]
                ]
            ]
        ]
    )
}


def checkOut(repo, branch, creds = 'jenkins-gh') {
    checkout(
        [
            $class: 'GitSCM',
            branches: [
                [
                    name: '*/' + branch
                ]
            ],
            doGenerateSubmoduleConfigurations: false,
            userRemoteConfigs: [
                [
                    credentialsId: creds,
                    url: repo
                ]
            ]
        ]
    )
}


def getEnvironmentFromBranch(branch) {
    def environmentMap = [
        "qa"      : "qa",
        "staging" : "staging",
        "master"  : "prod"
    ]
    return environmentMap.get(branch, "dev")
}


def getAWSAccountId(environment) {
    file = new File('./deployment_helper/aws_accounts.json')
    json = new JsonSlurper().parse(file)
    
    accountId = json[environment]?.account

    println "Account for ${environment}: ${accountId}"
    return accountId
}


def getJenkinsRoleArn(String account) {
    return "arn:aws:iam::${account}:role/jenkins-role"
}


Tuple getStsCreds(String environmentName) {
    String accountId = getAWSAccountId(environmentName)
    String roleArn = getJenkinsRoleArn(accountId)

    try {
        String cmd = "aws sts assume-role --role-arn ${roleArn} --role-session-name \"RoleSession1\" --output text" +
                " | awk 'END {print \$2 \"\\n\" \$4 \"\\n\" \$5}' > temp.txt"
        steps.sh(cmd)
    } catch (Exception e) {
        steps.println(e)
    }

    String key = steps.sh(returnStdout: true, script: 'head -1 temp.txt | tail -1 | tr -d "\n" ')
    String secret = steps.sh(returnStdout: true, script: 'head -2 temp.txt | tail -1 | tr -d "\n" ')
    String token = steps.sh(returnStdout: true, script: 'head -3 temp.txt | tail -1 | tr -d "\n" ')
    steps.sh("rm -f temp.txt")
    return [key, secret, token]
}
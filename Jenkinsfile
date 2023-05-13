pipeline {
    agent none
    parameters {
        string(name: 'test_suit_path', defaultValue: '.', description: 'which test(s) do you want to run? default is to run all tests (.)')
        choice(name: 'revision_type', choices: ['branch', 'hash', 'tag'], description: 'git revision type')
        string(name: 'revision_value', defaultValue: 'master', description: 'git revision value')
    }
    
    stages {
        stage('Test') {
            agent {label 'qms'}
            environment {
                TEST_RUN_NAME = "${JOB_NAME}_${BUILD_NUMBER}"
                DATE_ISO_FORMAT = """${sh(returnStdout: true, script: 'date +%Y-%m-%d | tr -d "\n"')}"""
                TEST_REPORT_URL = "http://192.168.1.47/reports/${DATE_ISO_FORMAT}/jenkins_${TEST_RUN_NAME}"
            }
            steps {
                script {
                    currentBuild.description = """Report path: <a href="${env.TEST_REPORT_URL}">Link</a> """
                    sh "python3 /home/pr/pr-docker-manager/exec_test.py -u jenkins -n ${TEST_RUN_NAME} -p sina-test-framework-samples -r ${params.revision_type} -v ${params.revision_value} -s ${params.test_suit_path}"
                }
            }
        }
    }
}

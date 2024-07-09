def USERNAME="olt_qa"
def TEST_RUN_NAME
def DATE_ISO_FORMAT

pipeline {
    agent {label 'qms'}
    
    parameters {
        string(name: 'test_suit_path', defaultValue: '.', description: 'which test(s) do you want to run? default is to run all tests (.)')
        choice(name: 'revision_type', choices: ['branch', 'hash', 'tag'], description: 'git revision type')
        string(name: 'revision_value', defaultValue: 'master', description: 'git revision value')
        string(name: 'ip_board', defaultValue: '.', description: 'board ip')
    }
    
    stages {
        stage('Test') {
            steps {
                script {
                    TEST_RUN_NAME = "${JOB_NAME}_${BUILD_NUMBER}"
                    DATE_ISO_FORMAT = """${sh(returnStdout: true, script: 'date +%Y-%m-%d | tr -d "\n"')}"""
                    TEST_REPORT_URL = "http://192.168.1.47/reports/${DATE_ISO_FORMAT}/${USERNAME}_${TEST_RUN_NAME}/build/html"
                    currentBuild.description = """Report path: <a href="${TEST_REPORT_URL}">Link</a> """
                    sshagent (credentials: ['olt_qa_qms_account']) {
                        sh "ssh -o StrictHostKeyChecking=no -p 5555 ${USERNAME}@192.168.1.47 qa -n ${TEST_RUN_NAME} -p test_sp5100_rest -r ${revision_type},${revision_value} -s \\\'--stepwise\\\' \\\'--cache-clear\\\' \"${test_suit_path}  ${ip_board}\" -vv || true"
                    }
                }
            }
        }
    }
    
    post {
        always {
            sh "rm -rf xml"
            sh "wget -P xml/ http://192.168.1.47/reports/${DATE_ISO_FORMAT}/${USERNAME}_${TEST_RUN_NAME}/xml/result.xml"
            junit testResults: 'xml/*.xml'
        }
    }
}

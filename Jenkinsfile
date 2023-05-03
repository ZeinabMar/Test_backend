pipeline {
    agent none
    stages {
        stage('Smoke Test') {
            agent {label 'qms'}
            steps {
                sh 'cd /home/pr/pr-docker-manager && sudo python3 ./execute_test.py jenkins test \"-m smoke samples/*\"'
            }
        }
        stage('Full Test') {
            agent {label 'qms'}
            steps {
                sh 'cd /home/pr/pr-docker-manager && sudo python3 ./execute_test.py jenkins test samples/*'
            }
        }
    }
}

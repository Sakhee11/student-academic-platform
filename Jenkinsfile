
pipeline {
    agent any

    stages {
        stage('SCM Checkout') {
            steps {
                echo 'Source code checked out by Jenkins'
                checkout scm
            }
        }

        stage('Python Setup') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Code Linting') {
            steps {
                sh '''
                    . venv/bin/activate
                    flake8 app/ database/ --count --select=E9,F63,F7,F82 --show-source --statistics
                '''
            }
        }

        stage('Automated Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    mkdir -p reports
                    pytest -v --cov=app \
                        --junitxml=reports/test-results.xml tests/
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true,
                  testResults: 'reports/test-results.xml'
        }

        success {
            echo 'Student Academic Platform CI completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}

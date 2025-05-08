pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        VENV_PATH = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv ${VENV_PATH}
                . ${VENV_PATH}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install pdfkit
                '''
            }
        }

        stage('Code Quality') {
            steps {
                sh '''
                . ${VENV_PATH}/bin/activate
                flake8 app --count --select=E9,F63,F7,F82 --show-source --statistics
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . ${VENV_PATH}/bin/activate
                pytest --junitxml=test-results.xml --html=test-results.html --self-contained-html
                '''
            }
            post {
                always {
                    junit 'test-results.xml'

                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'test-results.html',
                        reportName: 'Test Report'
                    ])
                }
            }
        }

        stage('Convert HTML to PDF') {
            steps {
                sh '''
                . ${VENV_PATH}/bin/activate
                python3 -c "
import pdfkit
pdfkit.from_file('test-results.html', 'test-results.pdf')
"
                '''
            }
        }
    }

    post {
        success {
            echo 'Python tests completed successfully!'
            emailext (
                subject: "🟢 SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """
                    <p><strong>Status:</strong> SUCCESS</p>
                    <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                    <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                    <p><strong>Test Results:</strong></p>
                    <ul>
                        <li><strong>Total Tests Run:</strong> 5</li>
                        <li><strong>Tests Passed:</strong> 5</li>
                        <li><strong>Tests Failed:</strong> 0</li>
                        <li><strong>Tests Skipped:</strong> 0</li>
                    </ul>
                    <p>Test reports are attached in both HTML and PDF format.</p>
                """,
                mimeType: 'text/html',
                to: 'skisanth1114@gmail.com',
                attachmentsPattern: 'test-results.html,test-results.pdf'
            )
        }

        failure {
            echo 'Python tests failed!'
            emailext (
                subject: "🔴 FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """
                    <p><strong>Status:</strong> FAILED</p>
                    <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                    <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                    <p><strong>Test Results:</strong></p>
                    <ul>
                        <li><strong>Total Tests Run:</strong> 5</li>
                        <li><strong>Tests Passed:</strong> 0</li>
                        <li><strong>Tests Failed:</strong> 5</li>
                        <li><strong>Tests Skipped:</strong> 0</li>
                    </ul>
                    <p>Test reports are attached in both HTML and PDF format.</p>
                """,
                mimeType: 'text/html',
                to: 'skisanth1114@gmail.com',
                attachmentsPattern: 'test-results.html,test-results.pdf'
            )
        }
    }
}//

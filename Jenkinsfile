pipeline {
    agent {
        docker {
            image 'python:3.7-alpine'
            args '-u root:root'
        }
    }
    stages {
        stage('checkout') {
            steps {
                checkout scm
            }
        }
        stage('Lint') {
            steps {
                sh 'flake8'
            }
        }
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python manage.py test'
            }
        }
    }
}
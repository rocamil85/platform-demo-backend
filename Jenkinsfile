pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: python
      image: python:3.12-slim
      command:
        - sleep
      args:
        - 99d
'''
        }
    }

    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verificar entorno') {
            steps {
                sh '''
                    echo "PIPELINE CI DEL BACKEND"
                    hostname
                    git rev-parse --short HEAD
                '''
            }
        }

        stage('Instalar dependencias') {
            steps {
                container('python') {
                    sh '''
                        python --version
                        python -m venv .venv
                        . .venv/bin/activate
                        python -m pip install --upgrade pip
                        pip install -r requirements-dev.txt
                    '''
                }
            }
        }

        stage('Calidad de código') {
            steps {
                container('python') {
                    sh '''
                        . .venv/bin/activate
                        ruff check .
                    '''
                }
            }
        }

        stage('Pruebas unitarias') {
            steps {
                container('python') {
                    sh '''
                        . .venv/bin/activate
                        pytest --cov=app_backend --cov-report=term-missing
                    '''
                }
            }
        }
    }
}

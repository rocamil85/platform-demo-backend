pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins-agent
  containers:
    - name: python
      image: python:3.12-slim
      command:
        - sleep
      args:
        - 99d

    - name: gcloud
      image: gcr.io/google.com/cloudsdktool/google-cloud-cli:stable
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

	stage('Construir y publicar imagen') {
            steps {
                script {
                    env.IMAGE_TAG = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                }

                container('gcloud') {
                    sh '''
                        echo "Verificando identidad de Google Cloud"
                        gcloud auth print-access-token > /dev/null

                        echo "Construyendo imagen con tag: ${IMAGE_TAG}"

                        gcloud builds submit . \
                          --config=cloudbuild.yaml \
                          --substitutions="_IMAGE_TAG=${IMAGE_TAG}" \
                          --project=project-965520fc-7451-4c3b-a07 \
                          --quiet
                    '''
                }
            }
        }
    }
}

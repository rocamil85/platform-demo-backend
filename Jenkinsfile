pipeline {
    agent {
        label 'platform-agent'
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

        stage('Verificar código') {
            steps {
                sh '''
                    echo "PIPELINE DEL BACKEND EJECUTÁNDOSE"
                    echo "Pod agente:"
                    hostname

                    echo "Directorio de trabajo:"
                    pwd

                    echo "Contenido descargado desde GitHub:"
                    ls -la

                    echo "Commit ejecutado:"
                    git rev-parse --short HEAD
                '''
            }
        }
    }
}

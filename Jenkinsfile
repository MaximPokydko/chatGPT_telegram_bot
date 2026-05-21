pipeline {
    agent any

    parameters {
        choice(
            name: 'ENV',
            choices: ['dev', 'prod'],
            description: 'Deployment environment'
        )
    }

    environment {
        IMAGE_NAME = "telegram-bot"
        CONTAINER_NAME = "tg-bot"
    }

    stages {

        stage('Clone Repository') {
            steps {
                echo 'Repository cloned successfully'
            }
        }

        stage('Show Environment') {
            steps {
                echo "Deploying to ${ENV}"
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $IMAGE_NAME .
                '''
            }
        }

        stage('Stop Old Container') {
            steps {
                sh '''
                    docker rm -f $CONTAINER_NAME || true
                '''
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                    docker run -d \
                    --name $CONTAINER_NAME \
                    -e TELEGRAM_BOT_TOKEN=123 \
                    -e OPENAI_API_KEY=123 \
                    $IMAGE_NAME
                '''
            }
        }

        stage('Check Container') {
            steps {
                sh '''
                    sleep 5
                    docker ps -a
                    docker logs $CONTAINER_NAME
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}

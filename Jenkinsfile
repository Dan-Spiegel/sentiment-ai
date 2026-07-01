pipeline {
  agent any

  environment {
    IMAGE_NAME   = 'ghcr.io/dan-spiegel/sentiment-ai'
    IMAGE_TAG    = "${env.BUILD_NUMBER}"
    TEST_IMAGE   = "sentiment-ai-test:${env.BUILD_NUMBER}"
    STAGING_NAME = 'sentiment-ai-staging'
  }

  options {
    timestamps()
    disableConcurrentBuilds()
  }

  stages {

    stage('1. Checkout') {
      steps {
        checkout scm
        sh 'git log -1 --oneline'
        sh 'echo "Commit SHA: $(git rev-parse HEAD)"'
      }
    }

    stage('2. Lint') {
      steps {
        sh 'docker build --target test -t ${TEST_IMAGE} .'
        sh 'docker run --rm ${TEST_IMAGE} flake8 app tests'
      }
    }

    stage('3. Build & Test') {
      steps {
        sh 'docker rm -f sentiment-ai-tests || true'
        sh 'docker run --name sentiment-ai-tests ${TEST_IMAGE} pytest --cov=app --cov-report=xml --cov-report=term'
        sh 'docker cp sentiment-ai-tests:/app/coverage.xml coverage.xml'
        sh 'docker rm -f sentiment-ai-tests'
        sh 'docker build --target runtime -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .'
      }
    }

stage('4. SonarQube') {
      steps {
        script {
          def scannerHome = tool 'sonar-scanner'
          withSonarQubeEnv('SonarQube') {
            sh """
              ${scannerHome}/bin/sonar-scanner \
                -Dsonar.projectKey=sentiment-ai \
                -Dsonar.sources=app \
                -Dsonar.tests=tests \
                -Dsonar.python.coverage.reportPaths=coverage.xml
            """
          }
        }
      }
    }

    stage('5. Quality Gate') {
      steps {
        timeout(time: 5, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
        }
      }
    }

    stage('6. Security Scan') {
      steps {
        sh '''
          docker run --rm \
            -v /var/run/docker.sock:/var/run/docker.sock \
            aquasec/trivy:latest image \
            --severity HIGH,CRITICAL \
            --no-progress \
            ${IMAGE_NAME}:${IMAGE_TAG}
        '''
      }
    }

    stage('7. Push') {
      when {
        anyOf {
          branch 'main'
          expression { (env.GIT_BRANCH ?: '').endsWith('main') }
        }
      }
      steps {
        withCredentials([usernamePassword(
            credentialsId: 'ghcr-credentials',
            usernameVariable: 'GHCR_USER',
            passwordVariable: 'GHCR_TOKEN')]) {
          sh 'echo $GHCR_TOKEN | docker login ghcr.io -u $GHCR_USER --password-stdin'
          sh 'docker push ${IMAGE_NAME}:${IMAGE_TAG}'
          sh 'docker push ${IMAGE_NAME}:latest'
        }
      }
    }

    stage('8. IaC Apply') {
      steps {
        dir('infra') {
          sh 'terraform init -input=false'
          sh 'terraform apply -auto-approve -input=false -var="image=${IMAGE_NAME}:${IMAGE_TAG}"'
          sh 'terraform output'
        }
      }
    }

    stage('9. Smoke Test') {
      steps {
        sh '''
          for i in $(seq 1 10); do
            if curl -fsS http://${STAGING_NAME}:8000/health; then
              echo ""
              echo "Staging is UP (200 OK)"
              exit 0
            fi
            echo "Waiting for staging... ($i)"
            sleep 3
          done
          echo "Smoke test FAILED"
          exit 1
        '''
      }
    }
  }

  post {
    always {
      sh 'docker rm -f sentiment-ai-tests || true'
      echo 'Pipeline termine.'
    }
  }
}

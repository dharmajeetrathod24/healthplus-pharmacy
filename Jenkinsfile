pipeline {
  agent any
  environment {
    IMAGE = "dharma2436/pharmacy"
    TAG   = "build-${BUILD_NUMBER}"
  }
  stages {
    stage('Unit Test') {
      steps {
        sh '''docker run --rm -u $(id -u):$(id -g) -e HOME=/tmp -e PYTHONDONTWRITEBYTECODE=1 -v $PWD:/src -w /src python:3.12-slim sh -c "pip install -q --user -r requirements.txt pytest && python -m pytest -q -p no:cacheprovider"'''
      }
    }
    stage('Docker Build') {
      steps { sh 'docker build -t $IMAGE:$TAG .' }
    }
    stage('Docker Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'U', passwordVariable: 'P')]) {
          sh 'echo $P | docker login -u $U --password-stdin'
          sh 'docker push $IMAGE:$TAG'
        }
      }
    }
    stage('Deploy to Kubernetes') {
      steps {
        sh 'sed -i "s|:IMAGE_TAG|:$TAG|" deploy/prod.yaml'
        sh 'kubectl apply -f deploy/prod.yaml'
        sh 'kubectl -n hp-prod rollout status deployment/pharmacy --timeout=300s'
      }
    }
  }
}

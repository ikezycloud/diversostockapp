pipeline {
  agent any

  triggers {
    pollSCM('*/5 * * * *') // Trigger the pipeline every 5 minutes
  }

  stages {
    stage('Checkout SCM') {
      steps {
        // Checkout the source code from SCM repository
        checkout scm
      }
    }


    stage('Deploy to Test Environment') {
      steps {
        // Deploy the Docker containers using Docker Compose
        sh 'docker-compose up -d'
      }
    }

    //stage('Push Docker Image') {
      //steps {
        // Push the Docker image to a Docker registry
        //withDockerRegistry(credentialsId: 'docker-hub-credentials', url: 'https://registry.hub.docker.com') {
          //sh 'docker tag stockbrokerapp_diversostockapp ikezycloud/diversostockapp:latest'
          //sh 'docker push ikezycloud/diversostockapp:latest'
        //}
      //}
    //}
  }
}

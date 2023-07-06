pipeline {
  agent any


    stage('Build Docker Image') {
      steps {
        // Build the Docker image using the Dockerfile
        sh 'docker build -t diversostockapp .'
      }
    }

    stage('Push Docker Image') {
      steps {
        // Push the Docker image to a Docker registry
        withDockerRegistry(credentialsId: 'docker-hub-credentials', url: 'https://registry.hub.docker.com') {
          sh 'docker push diversostockapp'
        }
      }
    }

    stage('Deploy to Test Environment') {
      steps {
        // Deploy the Docker containers using Docker Compose
        sh 'docker-compose up -d'
      }
    }
  }
}

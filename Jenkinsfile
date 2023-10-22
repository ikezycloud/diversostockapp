pipeline {
  agent any

  triggers {
    pollSCM('*/5 * * * *') // Trigger the pipeline every 5 minutes
  }

  stages {
    stage('Checkout SCM') {
      steps {
        checkout scm
      }
    }

    stage('Backup Database') {
      steps {
        script {
          def isContainerRunning = sh(script: 'sudo docker ps -q --filter "name=diversostockapp"', returnStatus: true)
          if (isContainerRunning == 0) {
            echo 'The container is not running. Using the last backup database.'
          } else {
            echo 'The container is running. Backing up the database.'
            sh 'docker cp diversostockapp:/diverso-stock-app/shares_broker/db.sqlite3 db_backup.sqlite3'
          }
          sh 'docker-compose down' // Stop containers
        }
      }
    }

    stage('Deploy to Test Environment') {
      steps {
        // Deploy the Docker containers using Docker Compose
        sh 'docker-compose up -d'
      }
    }

    stage('Restore Database') {
      steps {
        script {
          def isContainerRunning = sh(script: 'sudo docker ps -q --filter "name=diversostockapp"', returnStatus: true)
          if (isContainerRunning == 0) {
            echo 'The container is not running. Skipping database restoration.'
          } else {
            echo 'The container is running. Restoring the last backup database.'
            sh 'docker cp db_backup.sqlite3 diversostockapp:/diverso-stock-app/shares_broker/db.sqlite3'
          }
        }
      }
    }

    stage('Clean Up') {
      steps {
        sh 'rm db_backup.sqlite3'
      }
    }
  }
}

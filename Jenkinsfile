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

    stage('Backup Database'){
      steps {
        sh 'docker-compose down'
        sh 'docker cp diversostockapp:/diverso-stock-app/shares_broker/db/db.sqlite3 db_backup.sqlite3'
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
        sh 'docker cp db_backup.sqlite3 diversostockapp:/diverso-stock-app/shares_broker/db/db.sqlite3'
      }
    }

    stage('Clean Up') {
      steps {
        sh 'rm db_backup.sqlite3'
      }
    }
  }
}

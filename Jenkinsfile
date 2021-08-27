pipeline {

      agent any
      stages {
        stage('Clone sources') {
            steps {
                git branch: 'main', url : 'https://github.com/houssembenali/fil_rouge'
            }
        }
        
        stage('Package and deliver') {
            steps {
                sh 'gradle --version'
                sh 'gradle up'
            }
        }
      }
 }
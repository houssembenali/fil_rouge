pipeline {

      agent any
      stages {
        stage('Clone sources') {
            steps {
                git branch: 'main', url : 'https://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:x-oauth-basic@github.com/houssembenali/fil_rouge.git'
            }
        }
        
        stage('Package and deliver') {
             tools {
               gradle 'installGradle'
             }
            steps {
                sh 'gradle up'
            }
        }
      }
 }
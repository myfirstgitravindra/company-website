pipeline {
    agent any
    
    stages {
        stage('Git Checkout') {
            steps {
                git branch: 'main', 
                credentialsId: 'git-hub-cred', 
                url: 'https://github.com/myfirstgitravindra/company-website'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("ravindra806/company-website:${env.BUILD_ID}")
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-hub-creds', 
                        passwordVariable: 'PWD', 
                        usernameVariable: 'USR'
                    )]) {
                        sh """
                        docker login -u $USR -p $PWD
                        docker push ravindra806/company-website:${env.BUILD_ID}
                        """
                    }
                }
            }
        }
        
        stage('EKS-deploy') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'  
                ]]) {
                    sh '''
                        aws eks --region us-east-1 update-kubeconfig --name company-website-cluster
                        kubectl apply -f k8s/ --validate=false
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo '✅ Full CI/CD pipeline succeeded!'
        }
    }
}
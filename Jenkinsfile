def img
pipeline {
	environment {
    	registry = "dfortysix/python-cicd" //To push an image to Docker Hub, you must first name your local image using your Docker Hub username and the repository name that you created through Docker Hub on the web.
    	registryCredential = 'Dockerhub-xacthuc'
    	dockerImage = ''
	}
	agent any
	stages {
    	stage('checkout') {
        	steps {
            	git 'https://github.com/Dfortysix/cicd-flask.git'
        	}
    	}

    	stage ('Stop previous running container'){
        	steps{
            	sh returnStatus: true, script: 'docker stop $(docker ps -a | grep ${JOB_NAME} | awk \'{print $1}\')'
            	sh returnStatus: true, script: 'docker rmi $(docker images | grep ${registry} | awk \'{print $3}\') --force' //this will delete all images
            	sh returnStatus: true, script: 'docker rm ${JOB_NAME}'
        	}
    	}


    	stage('Build Image') {
        	steps {
            	script {
                	img = registry + ":${env.BUILD_ID}"
                	println ("${img}")
                	dockerImage = docker.build("${img}")
            	}
        	}
    	}



    	stage('Test - Run Docker Container on Jenkins node') {
       	steps {

            	sh label: '', script: "docker run -d --name ${JOB_NAME} -p 5000:5000 ${img}"
      	}
    	}

    	stage('Push To DockerHub') {
        	steps {
            	script {
                	docker.withRegistry( 'https://registry.hub.docker.com ', registryCredential ) {
                    	dockerImage.push()
                	}
            	}
        	}
    	}

    stage('Deploy to Test Server') {
    steps {
        script {
            def stopcontainer = "docker stop ${JOB_NAME}"
            def delcontName = "docker rm ${JOB_NAME}"
            def delimages = 'docker image prune -a --force'
            def drun = "docker run -d --name ${JOB_NAME} -p 5000:5000 ${img}"
            println "${drun}"
            sshagent(['qa-key']) {
                sh returnStatus: true, script: "ssh -o StrictHostKeyChecking=no ubuntu@47.128.222.116 ${stopcontainer} "
                sh returnStatus: true, script: "ssh -o StrictHostKeyChecking=no ubuntu@47.128.222.116 ${delcontName}"
                sh returnStatus: true, script: "ssh -o StrictHostKeyChecking=no ubuntu@47.128.222.116 ${delimages}"

                // some block
                sh "ssh -o StrictHostKeyChecking=no ubuntu@47.128.222.116 ${drun}"
            }
        }
    }
}


	}
}

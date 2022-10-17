//@Library('jenkinsLibs') _

pipeline {
    agent any
    options {
        timestamps()
        skipDefaultCheckout()
        disableConcurrentBuilds()
        timeout(time:1,unit:'HOURS')
    }

    stages {
         //gou jian构建
         stage('deploy') {
             steps {
                 timeout(time:20,unit:'MINUTES'){
                     script{
                    	sh "ls"
						if(env.BRANCH_NAME=="main"){
							 sh "echo 当前分支 : ${env.BRANCH_NAME}"
                    		 sh "echo 当前环境 : ${env.env}"
                    		 sh "echo 当前提交 : ${env.commit}"
                    		 sh "echo WORKSPACE : ${env.WORKSPACE}"
                    		 sh "echo GIT_BRANCH : ${env.GIT_BRANCH}"
                    		 sh "echo BUILD_NUMBER : ${env.BUILD_NUMBER}"
                    		 sh "echo JOB_NAME : ${env.JOB_NAME}"
							 sh "echo job:${env.PROJECT}"
							 sh "ls"
						}
	
					}
                 }
             }
         }
    }

    
    //构建后
     post{
        always{
            script{
                println('always')
            }
        }
        success{
            script{
                currentBuild.description='\n构建成功!'
            }
        }
        failure{
            script{
                currentBuild.description='\n构建失败!'
            }
        }
        aborted{
            script{
                currentBuild.description='\n构建取消!'
            }
        }
    }
}


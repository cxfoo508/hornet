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
							sh "docker-compose down --rmi all"
							sh "sh clear_iamges.sh"
							sh "docker-compose up -d"

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


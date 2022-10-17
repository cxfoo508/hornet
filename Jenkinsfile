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
                    	println("分支名称："+env.BRANCH_NAME) 
	
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


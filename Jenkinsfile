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
        //stage('GetCode') {
        //    steps {
		//		git branch: 'main', credentialsId: '123', url: 'https://github.com/cxfoo508/hornet.git'
        //        }
        //    }
         //gou jian构建
         stage('deploy') {
             steps {
                 timeout(time:20,unit:'MINUTES'){
                     script{
						sh "ll"
                        sh "docker-compose down --rmi all"
						sh "sh clear_iamges.sh"
						sh "docker-compose up -d"
                     }
                 }
             }
         }
        //test
        // stage('Test') {
        //     steps {
        //         timeout(time:20,unit:'MINUTES'){
        //             script{
        //                 println('ceshi start')
        //                 hello.printBuild('this is vars msg!!')
        //             }
        //         }
        //     }
        // }
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


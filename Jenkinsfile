@Library('jenkinsLibs') _

pipeline {
    agent any
    options {
        timestamps()
        skipDefaultCheckout()
        disableConcurrentBuilds()
        timeout(time:1,unit:'HOURS')
    }
    environment{
    }
    stages {
        stage('GetCode') {
            steps {
                
                timeout(time:5,unit:"MINUTES"){
                    script{
                      	sh 'echo ${env.BRANCH_NAME}'
			sh 'pwd'
			sh 'ls'
						
                    }
                }
            }
        }
        // //gou jian构建
        // stage('Build') {
        //     steps {
        //         timeout(time:20,unit:'MINUTES'){
        //             script{
        //                 println('构建代码')
        //             }
        //         }
        //     }
        // }
        // //test
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


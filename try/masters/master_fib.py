{
        '0'  : Node(File='codes/insert_number.py',inputs=[],args=[1],
            doc=('insert the value of 0th fibbonacci (1)')),
        '1'  : Node(File='codes/insert_number.py',inputs=[],args=[1],
            doc=('insert the value of 1th fibbonacci (1)')),
            
            
        '2'  : Node(File='codes/sum.py',inputs=['0','1']
            ,doc=('insert the value of 2th fibbonacci '
                'as the sum of the two previous numbers'
                ),),
        '3'  : Node(File='codes/sum.py',inputs=['1','2'],
            doc=('insert the value of 3th fibbonacci '
                'as the sum of the two previous numbers'
                ),),
        '4'  : Node(File='codes/slow_sum.py',inputs=['2','3'],
            doc=('insert the value of 4th fibbonacci '
                'as the sum of the two previous numbers'
                ),),
        '5'  : Node(File='codes/sum.py',inputs=['3','4'],
            doc=('insert the value of 5th fibbonacci '
                'as the sum of the two previous numbers'
                ),),
        '6'  : Node(File='codes/sum.py',inputs=['4','5'],
           doc=('insert the value of 6th fibbonacci '
                'as the sum of the two previous numbers'
                ),),
        '7':Node_bash(cmd='cat',inputs=['0','1','2','3','4','5','6'],
           doc=('join the seven firsts numbers of fibonacci into a file'
                ),),
 }

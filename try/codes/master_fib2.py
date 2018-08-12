
class g:
    def __getitem__(self,n):
        n=int(n)
        if n==0 or n==1:
            return Node(File='pruebas/insert_number.py',inputs=[],args=[1],
            doc=('insert the value of 0th fibbonacci (1)'))
        else:
            return  Node(File='pruebas/sum.py',inputs=list(map(g,(n-1),(n-2))),
           doc=('insert the value of 6th fibbonacci '
                'as the sum of the two previous numbers'
                ),)
    def getmd5s(self):
        return 1
ans=g()
g=g

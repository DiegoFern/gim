import gim
import pandas as pd
@gim._Master
def ins(a):
    return a


@gim._Master
def next_fib(a,b):
    return a+b
@gim._Master
def chain(*x):
    return pd.DataFrame(list(x),columns=['fib'])

@gim._Master
def to_str(x):
    return str(x)
r={}
r['n0']=ins('n0',0)
r['n1']=ins('n1',1)
r['n2']=next_fib('n2',r['n1'],r['n0'])
r['n3']=next_fib('n3',r['n2'],r['n1'])
r['n4']=next_fib('n4',r['n3'],r['n2'])
for i in range(5,30):
    r['n%s'%i]=next_fib('n',r['n%s'%(i-1)],r['n%s'%(i-2)],)
n_all=chain('n_all',*[r[('n%s'%s)] for s in range(30)],type_save='.csv')

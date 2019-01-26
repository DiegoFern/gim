import gestion_models

@gestion_models._Master
def ins(a):
    return a


@gestion_models._Master
def next_fib(a,b):
    return a+b
@gestion_models._Master
def to_str(x):
    return str(x)

n0=ins('n0',0)
n1=ins('n1',1)
n2=next_fib('n2',n1,n0)
n3=next_fib('n3',n2,n1)
n4=next_fib('n4',n3,n2)
n_4=to_str('n_4',n4)



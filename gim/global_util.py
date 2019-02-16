'''
this object represent the abstraction of a object which change in the calculus
internal or external (DDBB)
'''
from functools import *
class meta():
    def __init__(self,n,path=(),args=(),kargs=()):
        self.path=path
        self.dict={}
        self.kargs=kargs
        self.args=args
        self.n=(n)
        pass

    def __repr__(self):
        return 'go({},{},*{},**{})'.format(self.n,self.path,self.args,self.kargs)
    def calc(self):
        ans=self.n
        for m,k,a in zip(self.path,self.kargs,self.args):
            if m!='__call__':
                ans=ans.__getattribute__(m)(*a,**k)
            else:
                ans=ans(*a,**k)
        return ans
    def update(self,n,path,args,kargs):
        self.n=n;self.path=path;self.args=args;self.kargs=kargs

class go(meta):

    def __getattribute__(self,m,*args,**kargs):
        #print(m)
        #if m in ('__init__','__dict__','path','args','kargs','n','__repr__','__str__','calc'):
        #    return meta.__getattribute__(self,m)
        #return self.__dict__[m](self.n,self.path+(m,),self.args+(args,),self.kargs+(kargs,))
        if m in meta.__getattribute__(self,'dict',):
            return partial(meta.__getattribute__(self,'dict',)[m],self)
        return meta.__getattribute__(self,m)
    def __call__(self,*args,**kargs):
        return go(self.n,self.path+('__call__',),self.args+(args,),self.kargs+(kargs,))
    #def __getitem__(self,*args,**kargs ):
        #return go(self.n,self.path+('__getitem__',),self.args+(args,),self.kargs+(kargs,))
    #def __setitem__(self,*args,**kargs ):
        #meta.update(self,self.n,self.path+('__setitem__',),self.args+(args,),self.kargs+(kargs,))
    def __init__(self,n,path=(),args=(),kargs=(),types=None,):
        meta.__init__(self,n,path=(),args=(),kargs=(),)
        if types is None:
            types=n
        self.n=n;self.path=path;self.args=args;self.kargs=kargs;
        for i in set(dir(types))-set(dir(meta(None))):
            a='''def {i}(self,*args,**kargs):
    return go(self.n,self.path+(\'{i}\',),self.args+(args,),self.kargs+(kargs,),types={types})
#self.{i}={i}
self.dict[\'{i}\']=({i})
go.{i}={i}
    '''.format(i=i,types=types)

            exec(a)
    #if 1==1:
    #    def __add__(self,*args,**kargs):
            #return go(self.n,self.path+('__add__',),self.args+(args,),self.kargs+(kargs,))


class N:
    def __init__(self,n):
        self.n=n
    def __add__(self,a):
        return self.n+a

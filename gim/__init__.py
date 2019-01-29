import re,os,hashlib,inspect
from .utils import Node_function
import functools
class gim(dict):

    def __init__(self,
            ):
        pass

    def __call__(self,f):
        return Master(f)
    def get_dot(self,out=None,target=None,format_dot='dot',browser=False):
        D=self
        assert format_dot in ('dot','png','svg')
        if format_dot!='dot':
            out2=out
            out='/tmp/temp_dot'
        import sys
        D
        if target is not None:
            D={i:D[i] for i in D[target].get_children_names(target,D)}
        for d in D.values():
            d.getmd5s()
        import sys
        try:
            out=open(out,'w')
        except:
            pass
        f=out
        g=re.escape

        print('digraph{',file=f)
        if target:
            D={i:D[i] for i in D[target].get_children_names(target,D)}
        for k,v in D.items():
            print(v.getdot(k).strip(),file=f)
            for l in v.inputs_names:
                print('"{}"->"{}"'.format(g(l.File),g(k)),file=f)
        print('}',file=f)
        try:
            f.close()
        except:
            pass
        if format_dot!='dot':
            (os.system(' '.join(
            ['dot','-T'+format_dot,'/tmp/temp_dot']+(
                ['>',out2] if out2 else []
                ))))
        if browser:
            os.system('google-chrome {}'.format(out2))

 
gim=gim()
class _Master:

    def __init__(self,f):
        self.f=f
        
    def __call__(self,name,*args):
        I=len(args)
        for i,a in enumerate(args):
            if not (type(a)==Node_function):
                I=i
                break
        n=Node_function(File=name
                ,inputs=tuple((i for i in args[:I])),args=args[I:],
                node=name,
                master='.',
                fun=self.f,
                name=name,)
        n.getmd5s()
        gim[n.name]=n
        return n


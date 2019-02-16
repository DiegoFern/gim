import re,os,hashlib,inspect
from .utils import Node_function
import functools
from itertools import chain
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
        print_=print
        import sys
        try:
            out=open(out,'w')
        except:
            import tempfile
            out=[]
            print_=lambda x,**args:out.append(x)
        f=out
        g=re.escape
        print_('digraph{',file=f)
        for k,v in D.items():
            print_(v.getdot(k).strip(),file=f)
            for l in v.inputs_names:
                print_('"{}"->"{}"'.format(g(l.md5),g(v.md5)),file=f)
        print_('}',file=f)
        try:
            f.close()
        except:
            pass
            return '\n'.join(f)
        if format_dot!='dot':
            (os.system(' '.join(
            ['dot','-T'+format_dot,'/tmp/temp_dot']+(
                ['>',out2] if out2 else []
                ))))
        if browser:
            os.system('google-chrome {}'.format(out2))

 
gim=gim()
class _Master(object):

    def __init__(self,f):
        self.f=f
        
    def __call__(self,name,*args,type_save='.pkl',**kargs):
        #I=len(args)
        #for i,a in enumerate(args):
        #    if not (type(a)==Node_function):
        #        I=i
        #        break
        n=Node_function(File=name
                ,args=args,keyargs=kargs,
                node=name,
                master='.',
                fun=self.f,
                name=name,
                type_save=type_save)
        n.getmd5s()
        gim[n.md5]=n
        return n

class _Master_selfname(_Master):
    def __call__(self,*args,type_save='.pkl',**kargs):
        _Master.__call__(self.f.__name__,*args,type_save='.pkl',**kargs)


@_Master
def concatenate(name,*nodes):
    return

import itertools,re
FILENOTES=open('.log','a')
import hashlib,time,os,subprocess,datetime
def eval_(x,Node=None,master=None,out=None,):
    t1=time.clock()
    ans=1
    ans=os.system((x))
    
    if ans!=0:
        if out:
            os.remove(out)
        raise Exception('error '+x)
    t2=time.clock()
    return {'cmd':(x),'deltha_time':t2-t1,'Node':Node,'master':master,'time':datetime.datetime.now()}
def md5(fname):
    hash_md5 = subprocess.check_output(['md5sum', fname]).split()[0]
    return (hash_md5)

g=re.escape        
class Node:
    def __init__(self,File='',inputs=[],args=[],doc='',**kargs):
        self.file=File
        self.doc=doc
        self.args=args
        self.inputs=inputs
        self.inputs_names=inputs[:]
        self.md5=None
        self.md5file=None
        self.children_names=None
    def __repr__(self):
        return ('Node(%s)'%self.__dict__)
    def update_inputs(self,header) :
        self.inputs=[header+'.'+i for i in self.inputs]
        self.inputs_names=self.inputs[:]

    def getdot(self,name):
        color='red'
        if os.path.isfile('.data/'+self.md5):
            color='green'
        s='\n"{name}"[label=" node={name}\\nfile={file} \\nfileOut={md5} \\n{args}" fillcolor = {color} style=filled]'.format(
                md5=self.md5,file=g(self.file),
                name=g(name),args=g(repr(self.args)),color=color)
        return s
 
    def get_children(self):
        '''
        get all the nodes wich are need to calculate this Node
        '''
        return set([self])|set().union(*(i.get_children() for i in self.inputs))
    def get_children_names(self,d,D):
        if self.children_names is (None):
            self.children_names=set([d])|set().union(*(D[i].get_children_names(i,D) for i in self.inputs_names))
        return self.children_names
    
 
    def get_doc(self):
        Use=[]
        Args=[]
        ans="File: {}\nUse:{}\nArgs: {}\nOut:{}\nIs calculated:{}"
        for i in self.inputs_names:
            Use.append(i)
        for i in self.args:
            Args.append(i)
        return ans.format(
                self.file,
                ';'.join(Use),
               ';'.join(map(str,Args)),
               '.data/'+self.getmd5s(),
               os.path.isfile('.data/'+self.getmd5s())
               )
    def getmd5file(self):
        if self.md5file is None:
            self.md5file=md5(self.file)
        return self.md5file
    
    def getmd5s(self):
        if self.md5 is  None:
            self.md5='Out_%s'%((hashlib.sha224(str((md5(self.file),
                str(tuple(map(lambda x:x.getmd5s(),self.inputs))),
                str(tuple(map(str,self.args)))
                )
                
                ).encode('utf-8'))).hexdigest())
        return (self.md5)
    def update_insert(self,D):
        self.inputs=list(map(D.__getitem__,self.inputs))

    def start_time(self):
        return #time_data('times',{'file':self.file,'inputs'})
    
    def calculate(self):
        if os.path.isfile('.data/%s'%self.md5):
            return
        else:
            for i in self.inputs:
                i.calculate()
            
            print(eval_('python3 {}{}{} > {}'.format(
                self.file,
                append_head(' '.join(map(lambda x:'.data/%s'%x.md5,self.inputs))),
                append_head(' '.join(map(str,self.args))),
                '.data/%s'%self.md5,
                ),self.node,self.master),file=FILENOTES)
    def save_file(self,path):
        eval_('cp {} {}'.format(self.file,path))

    def track_savefile(self,g):
        return '{}|{}'.format(self.file,g)

class Node_bash(Node):

    def __init__(self,**args):
        super().__init__(**args)
        self.cmd=args['cmd']

    def calculate(self):
        if os.path.isfile('.data/%s'%self.md5):
            return
        else:
            for i in self.inputs:
                i.calculate()
            eval_('{}{}{} > {}'.format(
                
                self.cmd,
                append_head(' '.join(map(lambda x:'.data/%s'%x.md5,self.inputs))),
                append_head(' '.join(map(str,self.args))),
                '.data/%s'%self.md5,
                ))
    #def getmd5s(self):
    #    if self.md5 is  None:
    #        self.md5='Out_%s'%((hashlib.sha224(str((md5(self.cmd),
    #            str(tuple(map(lambda x:x.getmd5s(),self.inputs))),
    #            str(tuple(map(str,self.args)))
    #            )
    #            
    #            ).encode('utf-8'))).hexdigest())
    #    return (self.md5)

    def getmd5s(self):
        if self.md5 is  None:
            self.md5='Out_%s'%((hashlib.sha224(str((self.cmd,
                str(tuple(map(lambda x:x.getmd5s(),self.inputs))),
                str(tuple(map(str,self.args)))
                )
                
                ).encode('utf-8'))).hexdigest())
        return (self.md5)

    def getdot(self,name):
        color='red'
        if os.path.isfile('.data/'+self.md5):
            color='green'
        s='"{name}"[label=" node={name}\\ncmd={cmd} \\nfileOut={md5} \\n{args}" fillcolor = {color} style=filled]'.format(
                md5=self.md5,file=self.file,cmd=self.cmd,
                name=g(name),args=g(repr(self.args)),color=color)
        return s
    def get_doc(self):
        Use=[]
        Args=[]
        ans="Use: {}\nArgs: {}\nCmd: {}\nOut:{}\nIs calculated:{}"
        for i in self.inputs_names:
            Use.append(i)
        for i in self.args:
            Args.append(i)
        return ans.format(';'.join(Use),
               ';'.join(map(str,Args)),
               self.cmd,
               '.data/'+self.getmd5s(),
               os.path.isfile('.data/'+self.getmd5s())
               )

class Node_import(Node):
    def __init__(self,master,name_node_master):
        self.Graph=eval(open(master,'r'))
        node=self.Graph[name_node_master]
        self.node=node

def Grid(type,inputs,args,**kargs):
    Ans={}
    for i in itertools.product(*inputs):
        for j in itertools.product(*args):
            I=i+j
            Ans['.'.join(map(str,I))]=type(inputs=i,args=j,**kargs)
    return Ans






def append_head(x):
    if x:
        return ' %s'%x
    return x

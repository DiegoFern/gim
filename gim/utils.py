import itertools,re,pickle,inspect
FILENOTES=open('.log','a')
import hashlib,time,os,subprocess,datetime
def union(*dicts):
    return dict(itertools.chain.from_iterable(dct.items() for dct in dicts))

def eval_(x,Node=None,master=None,out=None,):
    t1=datetime.datetime.now()
    ans=1
    ans=os.system((x))
    
    if ans!=0:
        print(x,out)
        if out:
            os.remove(out.replace('.data','.calculating',))
        raise Exception('error '+x)
    t2=datetime.datetime.now()
    os.rename(out.replace('.data','.calculating',),out,)
    return {'cmd':(x),'deltha_time':format(t2-t1),'Node':Node,'master':master,'time':datetime.datetime.now()}

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    hash_md5 = subprocess.check_output(['md5sum', fname]).split()[0]
    return (hash_md5)

g=re.escape        

import csv
def eval_query(con=None,query=None,out=None,master=None):
    try:
        t1=datetime.datetime.now()
        with open('.calculating/'+out, 'w' ) as csvfile:
            c=con.cursor()
            c.execute(query)
            D = c.fetchall()
            spam_writer = csv.writer(csvfile, delimiter=';', lineterminator='\n')
            spam_writer.writerow([i[0] for i in c.description] )
            for d in D:
                spam_writer.writerow(d)
            c.close()
        os.rename('.calculating/'+out,'.data/'+out,)
        t2=datetime.datetime.now()
    except:
        os.remove('.calculating/'+out,)
        raise Exception('Failed query')
    return {'query':(query),'deltha_time':format(t2-t1),'Node':Node,'master':master,'time':datetime.datetime.now()}

class Node(object):
    def __init__(self,File='',inputs=[],args=[],doc='',
            stdout=True,txt=False,md5=None,
            **kargs):
        #if stdout=True its supossed that the command of the file
        #has as output the last args (py imp1...imp_M a.py arg1 arg2 ...argn output
        # in the other
        self.File=File
        self.txt=txt
        self.doc=doc
        self.stdout=stdout
        self.args=args
        self.inputs=inputs
        self.inputs_names=inputs[:]
        self.md5=md5
        self.md5file=None
        self.children_names=None
    def __repr__(self):
        return ('Node(**%s)'%self.__dict__)
    def update_inputs(self,header) :
        self.inputs=[header+'.'+str(i) for i in self.inputs]
        self.inputs_names=self.inputs[:]

    def getdot(self,name):
        color='red'
        if os.path.isfile('.data/'+self.md5):
            color='green'
        if os.path.isfile('.calculating/'+self.md5):
            color='yellow'
        s='\n"{name}"[label=" node={name}\\nfile={file} \\nfileOut={md5} \\n{args}" fillcolor = {color} style=filled]'.format(
                md5=self.md5,file=g(self.File),
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
                self.File,
                ';'.join(Use),
               ';'.join(map(str,Args)),
               '.data/'+self.getmd5s(),
               os.path.isfile('.data/'+self.getmd5s())
               )
    def getmd5file(self):
        if self.md5file is None:
            self.md5file=md5(self.File)
        return self.md5file
    
    def getmd5s(self):
        if self.md5 is  None:
            self.md5='Out_%s'%((hashlib.sha224(str((md5(self.File),
                str(tuple(map(lambda x:x.getmd5s(),self.inputs))),
                str(tuple(map(str,self.args)))
                )
                
                ).encode('utf-8'))).hexdigest())
        return (self.md5)

    def update_insert(self,D):
        self.inputs=list(map(D.__getitem__,self.inputs))

    def start_time(self):
        return #time_data('times',{'file':self.file,'inputs'})
    
    CMD="python3"
    
    def calculate(self):
        if os.path.isfile('.data/%s'%self.md5):
            return
        else:
            for i in self.inputs:
                i.calculate()
            scape_unix=str if os.name == 'nt' else "'{}'".format
            print(eval_('{CMD} {}{}{} {output}{}'.format(
                self.File,
                append_head(' '.join(map(lambda x:'.data/%s'%x.md5,self.inputs))),
                append_head(' '.join(map(
                    repr_,map(scape_unix,self.args)))),
                '.calculating/%s'%self.md5,
                output='> ' if self.stdout else '',

                CMD=self.CMD
                ),
                
                self.node,self.master,'.data/%s'%self.md5),file=FILENOTES)
    def save_file(self,path):
        eval_('cp {} {}'.format(self.File,path))

    def track_savefile(self,g):
        return '{}|{}'.format(self.File,g)
def md5_func(f):
    return hashlib.sha224(inspect.getsource(f).encode('utf-8')).hexdigest()

class Node_function(Node):
    def __init__(self,File='',inputs=[],args=[],doc='',
            stdout=True,txt=False,md5=None,
            name=None,fun=None,master='.',
            **kargs):
        #if stdout=True its supossed that the command of the file
        #has as output the last args (py imp1...imp_M a.py arg1 arg2 ...argn output
        # in the other
        self.File=File
        self.txt=txt
        self.doc=doc
        self.stdout=stdout
        self.args=args
        self.inputs=inputs
        self.inputs_names=inputs[:]
        self.md5=md5
        self.md5file=None
        self.children_names=None
        self.node=name
        self.master='.'
        self.fun=fun
        self.name=name

    def getdot(self,name):
        color='red'
        print(self.md5)
        if os.path.isfile('.data/'+self.md5+'.pkl'):

            color='green'
        if os.path.isfile('.calculating/'+self.md5+'.pkl'):
            color='yellow'
        s='\n"{name}"[label=" node={name}\\nfile={file} \\nfileOut={md5} \\n{args}" href=\"/calc/{name}\" fillcolor = {color} style=filled]'.format(
                md5=self.md5,file=g(self.File),
                name=g(name),args=g(repr(self.args)),color=color)
        return s
 

    def getmd5s(self):
        if self.md5 is  None:
            self.md5='Out_%s'%((hashlib.sha224(str((md5_func(self.fun),
                str(tuple(map(lambda x:x.getmd5s(),self.inputs))),
                str(tuple(map(str,self.args)))
                )
                
                ).encode('utf-8'))).hexdigest())
        return (self.md5)

    def calculate(self):
        pkl='.pkl'
        if os.path.isfile('.data/%s'%self.md5+pkl):
            return pickle.load(open('.data/%s'%self.md5+pkl,'rb')) 
        else:
            for i in self.inputs:
                i.calculate()
            #scape_unix=str if os.name == 'nt' else "'{}'".format
            out=self.fun(*(self.args+tuple((i.calculate())
                for i in self.inputs)))
            with open('.data/%s'%self.md5+pkl,'wb') as f: 
                pickle.dump(out,f)
            return (out)

class NodeR(Node):
    CMD="Rscript"

class inp(Node):
    pass
def repr_(s):
    if s and s[0]=='-':
        return s
    else:
        return str(s)


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
                append_head(' '.join(map(repr_,map(str,self.args)))),
                '.calculating/%s'%self.md5,
                ),out='.data/%s'%self.md5)
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
                md5=self.md5,file=self.File,cmd=self.cmd,
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

class Query(Node):
    CON={}
    def __init__(self,query='',con='',master=None,data_con={},doc='',
            tipe='sqlite',**kargs):
        assert tipe in ('sqlite','oracle'),'type of conexion not valid'
        if tipe=='sqlite':
            import sqlite3 as conexion
        elif tipe=='oracle':
            if con not in self.CON:
                import jpype
                import jaydebeapi as conexion
    
                from os.path import expanduser
                classpath = expanduser("~\\Downloads\\ojdbc6.jar")
                jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=%s" % classpath)
            
        elif tipe=='':
            pass
        
        self.Query=query
        self.md5=None
        self.md5file=None
        self.inputs_names=[]
        self.children_names=None
        self.inputs=[]
        if con not in self.CON:
            self.CON[con]=conexion.connect(**data_con)
        self.args=[]
        self.doc=doc
        self.con=con
        self.File=query#Query is seen like the code in herence context of a Node
    
    def __repr__(self):
        return ('Node(**%s)'%self.__dict__)

    def getmd5s(self):
        if self.md5 is  None:
            self.md5='Out_%s'%((hashlib.sha224(str((self.Query,
                str(tuple(map(lambda x:x.getmd5s(),self.inputs))),
                str(tuple(map(str,self.args)))
                )
                
                ).encode('utf-8'))).hexdigest())
        return (self.md5)

    
    def calculate(self):
        if os.path.isfile('.data/%s'%self.md5):
            return
        else:
            for i in self.inputs:
                i.calculate()
            
            print(eval_query(
               con = self.CON[self.con],
               query = self.Query,
               out= self.md5
                ),file=FILENOTES)
    def getdot(self,name):
        color='red'
        if os.path.isfile('.data/'+self.md5):
            color='green'
        if os.path.isfile('.calculating/'+self.md5):
            color='yellow'
        s='\n"{name}"[label=" node={name}\\nquery={file} \\nfileOut={md5} \\n{args}" fillcolor = {color} style=filled]'.format(
                md5=self.md5,file=(self.File.replace('\n','\\n')),
                name=g(name),args=g(repr(self.args)),color=color)
        return s
 


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

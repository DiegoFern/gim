from pprint import pprint
import sys
from utils import *
from compile_master import compile_master 
def to_commit(name_commit,output):
    assert os.path.isfile(name_commit),'commit doesn\'t exists'
    print(name_commit)
    path=name_commit.split('/')
    path='/'.join(path[:-2])
    print(path)
    if path:
        path=path+'/'
    print(path)
    input_=[]
    f=open(''+name_commit,'r')
    for i in f:
        if i.strip()!='-'*20:
            input_.append(i)
        else:
            break

    for dir,file in set(map(lambda x:tuple(x.strip().split('|')),
                       input_ )):
        print('cp {} {}'.format(path+'.savefiles/'+file,dir))
        os.system('cp {} {}'.format(path+'.savefiles/'+file,dir))
    with open(output,'w') as f2:
        for l in f:
            print(l,file=f2,end='')

def g(s):

    s=s.replace('[','\\[')
    s=s.replace(']','\\]')
    s=s.replace("'","\\'")
    s=s.replace("\"",r'''\"''')
    s=s.replace(",","\\,")
    return s
def commit(target,name_commit,inp):
    '''
    create a commit of all files into getting a target
    This information is registered in a hidden files of
    the proyect, a:
        .file2name->names of the file
        .execution->has the information about the different paths of the the ejecution
    and the files are save in folder:
        .savefiles
    in order to avoid overwrite the documents in savefiles it'll use the hash of that
    file. This helps to the algoritm to realize if a file version was saved in the past
    '''
    import sys
    D=compile_master(inp)
    for d in D.values():
        d.update_insert(D)
    import sys

    target=D[target]

    tracks=[]
    with open('.commit/{}'.format(name_commit),'w') as f:
        s=set()
        for node in (target.get_children()):
            if isinstance(node,Node_bash):
                continue
            g=str(node.getmd5file())[2:-1]
            if g in s:
                continue
            s.add(g)
            
            if not os.path.isfile('.savefiles/'+g):
                node.save_file('.savefiles/'+g)
            print(node.track_savefile(g),file=f)
        print('-'*20,file=f)
        print(inp,file=f)
    
def logging(log,output):
    rows=['Node','cmd','master','deltha_time','time',]
    if output:
        output=open(output,'w')
    else:
        output=None
    with output as F:
        print(*rows,sep='\t',file=F)
        for i in open('.log'):
            f=eval(i).get
            print(*list(map(f,rows)),sep='\t',file=F)

def read_log(log,target,output):
    G={}
    F={}
    for i in open('.log','r'):
        I=eval(i)
        cmd=I['cmd'].split()
        out=cmd[-1]
        inputs=cmd[2:-2]
        G[out]=(I,inputs)
        F[out]=i
        if out==target:
            break
    def get_nodes_rec(G,out):
        A=[]
        A.append(out)
        try:
            inputs=G[out]
            inputs=inputs[1]
        except:
            return []
        for Input in inputs:
            A.extend(get_nodes_rec(G,Input))
        return A
    for i in get_nodes_rec(G,target):
        print(F[i],end='')
    #pprint({i:G[i] for i in get_nodes_rec(G,target)})

def import_commit(name_commit,output):
    assert os.path.isfile(name_commit),'commit doesn\'t exists'
    print(name_commit)
    commit=name_commit.split('/')[-1]
    path=name_commit.split('/')
    path='/'.join(path[:-2])
    print(path)
    if path:
        path=path+'/'
    print(path)
    input_=[]
    f=open(''+name_commit,'r')
    for i in f:
        if i.strip()!='-'*20:
            input_.append(i)
        else:
            break
    for dir,file in set(map(lambda x:tuple(x.strip().split('|')),
                       input_ )):
        print('cp {} {}'.format(path+'.savefiles/'+file,'.savefiles/'+file))
        os.system('cp {} {}'.format(path+'.savefiles/'+file,'.savefiles/'+file))
    os.system('cp {} {}'.format(name_commit,output))
    
def compute(target,out,inp,master_name):
    import sys

    D=compile_master(inp)
    for nn,d in D.items():
        d.update_insert(D)
        d.node=nn
        d.master=master_name
    import sys

    target=D[target]


    target.getmd5s()
    target.calculate()
    if out is not None:
        f=open(out,'w')
    else:
        f=None
    for line in open('.data/'+target.md5):
        print(line,file=out,end='')
    if out:
        f.close()

def create_doc(inp,out,target):
    D=compile_master(inp)

    if out is not None:
        out=open(out,'w')
    if target:
        D={i:D[i] for i in D[target].get_children_names(target,D)}
     
    for d,n in sorted(D.items(),key=lambda x:x[0]):
        n.update_insert(D)
    for d,n in sorted(D.items(),key=lambda x:x[0]):
     
        print(' * ',d,' : ',n.doc.replace('\n','\n    '),sep='',file=out)
        print(' '*6,n.get_doc().replace('\n','\n      '),sep='',file=out)
        print('',file=out)

    if out is not None:
        out.close()

def import_computes(inp,repository):
    D=compile_master(inp)

    
    for d,n in sorted(D.items(),key=lambda x:x[0]):
        n.update_insert(D)
        os.system('cp {} {}'.format(
            repository+n.getmd5s() ,n.getmd5s()
            ))
        



def get_dir(target,inp
        ):
    import sys
    D=compile_master(inp)
    for d in D.values():
        d.update_insert(D)
    if target:
        print( 'data/'+D[target].getmd5s())
    else:
        for i in D:
            print(i, 'data/'+D[i].getmd5s(),sep='\t')

def get_dot(out,format_dot,inp,browser,target
        ):
    assert format_dot in ('dot','png','svg')
    if format_dot!='dot':
        out2=out
        out='/tmp/temp_dot'
    import sys
    D=compile_master(inp)
    if target:
        D={i:D[i] for i in D[target].get_children_names(target,D)}
     

    for d in D.values():
        d.update_insert(D)
    for d in D.values():
        d.getmd5s()
    import sys
    try:
        out=open(out,'w')
    except:
        pass
    f=out

    print('digraph{',file=f)
    if target:
        D={i:D[i] for i in D[target].get_children_names(target,D)}
    for k,v in D.items():
        print(v.getdot(k),end='',file=f)
        for l in v.inputs_names:
            print('"{}"->"{}"'.format(g(l),g(k)),file=f)
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

def parse(argv):
    from optparse import OptionParser
    usageStr = """
    USAGE:      python intelligent_model2 < master [options] >out
    """
    parser = OptionParser(usageStr)
    #parser.add_option('-n', '--numGames', dest='numGames', type='int',
    #                  help=default('the number of GAMES to play'),
    #                  metavar='GAMES', default=v1)
    parser.add_option('-g','--dot',dest='dot',action='store_true',default=False,
            help=('draw a graph of the nodes and the uses and his args, if you fixed a target '
                'the program will draw only the needed nodes. The command -f select the format ')
            )

    parser.add_option('-t','--target',dest='target',type=str,default='',
            help='put the node objetive to be calculated'
            )
    parser.add_option('-m','--master',dest='master',type=str,default='',
            help='file with the computes\' instruccions ')
    parser.add_option('--init',dest='init',action='store_true',default=False)
    parser.add_option('--gd',dest='_get_dir',action='store_true',default=False)
    parser.add_option('-o','--output',dest='output',type=str)
    parser.add_option('-f','--format_dot',dest='format_dot',type=str,default='dot')
    parser.add_option('--tc','--to_commit',dest='to_commit_',type=str,default='')
    parser.add_option('-b','--browser',dest='browser',action='store_true',default=False)
    parser.add_option('-c','--commit', dest='commit', type='str', default='')
    parser.add_option('--ic',dest='import_commit',type=str,default='')
    parser.add_option('-d',dest='doc',action='store_true',default=False)
    parser.add_option('-i',dest='import_computes',default='',type=str)
    parser.add_option('-l',dest='log',default=0,type=int)
    parser.add_option('-r',dest='read_log',default=None,type=str)
    return parser.parse_args(argv)

def main(dot,init,import_commit_,log,commit_,to_commit_,doc,target,master,output,format_dot,_get_dir,browser,import_computes_,_read_log):
    if init:
        print(os.system('ls'))
        os.system('mkdir .data')
        os.system('mkdir masters')
        os.system('mkdir codes')
        return
    if to_commit_:
        to_commit(to_commit_,output)
        return  
    if _read_log:
        read_log(log,target,output)
        return 
    if log:
        logging(log,output)
    if import_commit_:
        import_commit(import_commit_,output)
        return 
    inp=open(master,'r').read()
    if import_computes_:
        import_computes(inp,import_computes_)
    if doc:
        create_doc(inp,output,target)
        return 
    
    if commit_:
        commit(target,commit_,inp)
        return 
    if _get_dir:
        get_dir(target,inp)
        return 
 
    if not commit_ and dot:
        #out,format_dot,inp,browser,target
        get_dot(output,format_dot,inp,browser,target)
        return 
    if not commit_ and target:
        compute(target,output,inp,master)
    
if __name__=='__main__':
    import os
    args=(parse(sys.argv)[0])
    kargs={'output':args.output,'target':args.target,'_read_log':args.read_log,
            'dot':args.dot,'_get_dir':args._get_dir,'import_commit_':args.import_commit,
            'browser':args.browser,'master':args.master,
            'format_dot':args.format_dot,'commit_':args.commit,'init':args.init ,'to_commit_':args.to_commit_,'doc':args.doc,
            'import_computes_':args.import_computes,'log':args.log}
    main(**kargs)

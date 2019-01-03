import subprocess    
from itertools import chain
from flask import Flask,render_template,flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import platform
from flask import send_file
import os
import sys 
import time


app=Flask(__name__)
A='../try'
A='.'

def union(*dicts):
    return dict(chain.from_iterable(dct.items() for dct in dicts))
class rep:
    def __init__(self,name):
        self.name=name
    def __call__(self,*args,**kargs):
        return '{}({})'.format(self.name,
            ','.join(chain(map(str,args),(map(lambda x:'{}={}'.format(*x),
                kargs.items())))))

def get_date(x):
    """
        Try to get the date that a file was created, falling back to when it was
        last modified if that isn't possible.
        See http://stackoverflow.com/a/39501288/1709587 for explanation.
    
    """
    path_to_file='.data/'+x
    try:
        
        return time.ctime(os.stat('.data/'+x)[8])
    except FileNotFoundError:
        return "not_found"


inp=rep('inp')
Query=rep('Query')
Node=rep('Node')
NodeR=rep('NodeR')
Node_bash =rep('Node_bash') 
codes=[]
def pp(x,y):
    return x
for i in os.listdir(A+'/codes/'):
    text=open(A+'/codes/'+i,'r').read()
    link='/codes/'+i
    codes.append((i,text,link))
masters=[]

for i in os.listdir(A+'/masters/'):
    text=open(A+'/masters/'+i,'r').read()
    try:
        aux = eval(( 
            (subprocess.run(
            ['python3',os.path.dirname(os.path.abspath(__file__)),'-m',os.getcwd()+'/masters/'+i,'--md5'],
            
            check=True, stdout=subprocess.PIPE).stdout).decode("utf-8")))
    except:
        print('i failed',i)
        aux={}
    keys=sorted(map(
        lambda x:(x[0],
            'exec/{i}/{c}'.format(i=i,c=x[0]),
            x[1],
            ((x[1])[:3]=='inp'),
        

       get_date(aux[x[0]]) ),eval(text).items()) 
        
        ,key=lambda x:x[0]
            
        
        )

    link='/codes/'+i
    masters.append((i,text,link,keys,
        
        ))

@app.route('/',methods =['GET','POST'] )
def index():
    global codes,masters
    if request.method=='GET':
        return render_template('index.html',
            codes=codes,
            masters=masters)
    else:
        import pprint
        d=request.files.items()
        nodes=[]
        for name_file,File in (iter(d)):
            
            _,master,node=name_file.split('/')
            out=(subprocess.run(['python3',os.path.dirname(os.path.abspath(__file__)),'-m',os.getcwd()+'/masters/'+master,'-t',node,'--md5'],  check=True, stdout=subprocess.PIPE).stdout).decode("utf-8").strip()
            nodes.append('<li>{}:({})>{}</li>'.format(node,master,out))
            out='.data/'+out
            File.save(out)
        codes=[]
        for i in os.listdir(A+'/codes/'):
            text=open(A+'/codes/'+i,'r').read()
            link='/codes/'+i
            codes.append((i,text,link))
        masters=[]

        for i in os.listdir(A+'/masters/'):
            text=open(A+'/masters/'+i,'r').read()
            try:
                aux = eval(( 
                    (subprocess.run(
                    ['python3',os.path.dirname(os.path.abspath(__file__)),'-m',os.getcwd()+'/masters/'+i,'--md5'],
                    
                    check=True, stdout=subprocess.PIPE).stdout).decode("utf-8")))
            except:
                print('i failed',i)
                aux={}
            keys=sorted(map(
                lambda x:(x[0],
                    'exec/{i}/{c}'.format(i=i,c=x[0]),
                    x[1],
                    pp((x[1])[:3]=='inp',(x[1])[:3]=='inp'),
                

               get_date(aux[x[0]]) ),eval(text).items()) 
                
                ,key=lambda x:x[0]
                    
                
                )

            link='/codes/'+i
            masters.append((i,text,link,keys,
                
                ))

        return '''<h1>Updates:</h1>
        <ul>{}</ul>
        <a href='/'>back </a>'''.format(' '.join(nodes))

@app.route('/masterdoc/<master>')
def master(master):
    from __main__ import get_dot
    
    get_dot('/tmp/'+master+'.svg','svg',open('masters/'+master,'r').read(),False,None)
    return render_template('master.html',
            master=(open('/tmp/'+master+'.svg').read()))

@app.route('/codes/<name>')
def code(name):
    name=A+'/codes/'+name
    text=open(name,'r').read()
    print(text)
    return render_template('code.html',
            file=name,
            text=text,
            path=name)

@app.route('/exec/<master>/<t>')
def execute(master,t):
    aux = ['python3',os.path.dirname(os.path.abspath(__file__)),'-m',os.getcwd()+'/masters/'+master,'-t',t,'-q']
    print(*aux)
    out=(subprocess.run(aux,  check=True, stdout=subprocess.PIPE).stdout).decode("utf-8")
    out=out.split()
    print('====================>')
    print(out)
    if len(out)>1:
        print('====================>')
        return open(os.getcwd()+'/'+out[0],'r').read()
    out=os.getcwd()+'/'+out[0]
    return send_file(out ,attachment_filename=t[-1])

def run():
    app.run(debug=True)



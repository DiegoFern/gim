import subprocess    
from itertools import chain
from flask import Flask,render_template
from flask import send_file
import os
import sys 
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

Query=rep('Query')
Node=rep('Node')
NodeR=rep('NodeR')
Node_bash =rep('Node_bash') 
codes=[]
for i in os.listdir(A+'/codes/'):
    text=open(A+'/codes/'+i,'r').read()
    link='/codes/'+i
    codes.append((i,text,link))
masters=[]
for i in os.listdir(A+'/masters/'):
    text=open(A+'/masters/'+i,'r').read()
    keys=sorted(map(lambda x:(x[0],'exec/{i}/{c}'.format(i=i,c=x[0])
        ,x[1]),
        eval(text).items()),key=lambda x:x[0])

    link='/codes/'+i
    masters.append((i,text,link,keys))

@app.route('/', )
def index():
    return render_template('index.html',
            codes=codes,
            masters=masters)

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
    print(*[os.path.dirname(os.path.abspath(__file__)),'-m',os.getcwd()+'/masters/'+master,'-t',t],sep=' ')
    out=(subprocess.run(['python3',os.path.dirname(os.path.abspath(__file__)),'-m',os.getcwd()+'/masters/'+master,'-t',t,'-q'],  check=True, stdout=subprocess.PIPE).stdout).decode("utf-8").strip()
    out=os.getcwd()+'/'+out
    return send_file(out ,attachment_filename=t[-1])

def run():
    app.run()



import subprocess    
from flask import Flask,render_template
from flask import send_file
import os
import sys 
app=Flask(__name__)
A='../try'
A='.'

def Node(*args,**kargs):
    return 

Query=Node=Node_bash=Node
codes=[]
for i in os.listdir(A+'/codes/'):
    text=open(A+'/codes/'+i,'r').read()
    link='/codes/'+i
    codes.append((i,text,link))
masters=[]
for i in os.listdir(A+'/masters/'):
    text=open(A+'/masters/'+i,'r').read()
    keys=list(map(lambda x:(x,'exec/{i}/{c}'.format(i=i,c=x)),
        eval(text).keys()))

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



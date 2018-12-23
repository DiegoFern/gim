from flask import Flask,render_template
import os
import sys 
app=Flask(__name__)
A='../try'
A='.'
codes=[]
for i in os.listdir(A+'/codes/'):
    text=open(A+'/codes/'+i,'r').read()
    link='/codes/'+i
    codes.append((i,text,link))
masters=[]
for i in os.listdir(A+'/masters/'):
    text=open(A+'/masters/'+i,'r').read()
    masters.append((i,text))

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

def run():
    app.run()



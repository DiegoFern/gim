from flask import Flask,render_template
import os
import sys 
app=Flask(__name__)
A='../try'
codes=[]
for i in os.listdir(A+'/codes/'):
    text=open(A+'/codes/'+i,'r').read()
    link='/codes/'+i
    codes.append((i,text,link))
masters=[]
for i in os.listdir(A+'/masters/'):
    text=open(A+'/masters/'+i,'r').read()
    masters.append((i,text))

@app.route('/')
def index():
    return render_template('index.html',
            codes=codes,
            masters=masters)

@app.route('/codes/<name>')
def code(name):
    name=A+'/codes/'+name
    text=open(name,'r').read()
    print(text)
    return render_template('code.html',
            file=name,
            text=text,
            path=name)



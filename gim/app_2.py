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

dot=''
s=None
def run(server):
    global dot,s
    print(server)
    sys.path.append(os.getcwd())
    g=__import__(server.split('.')[0])

    s=g.gim.gim
    print('-------------------------')
    print(dot)
    app.run()

@app.route('/',methods =['GET','POST'] )
def index():
    dot=s.get_dot(format_dot='dot')
    return render_template('dot_read_2.html',graph=dot
            )

@app.route('/calc/<node>')
def calc(node):
    return '<pre><code> {}</code></pre>'.format((s[node].calculate()))


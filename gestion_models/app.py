import filehelpers as fh
import hashlib
import config    
import subprocess    
from itertools import chain
from flask import Flask,render_template,flash, request, redirect, url_for, abort, make_response
from werkzeug.utils import secure_filename
import platform
from flask import send_file
import os
import sys 
import time
from collections import namedtuple
masters=[
        ]
codes=[]

app=Flask(__name__)
root ='.'

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

NODES={
'inp':rep('inp'),
'Query':rep('Query'),
'Node':rep('Node'),
'NodeR':rep('NodeR'),
'Node_bash' :rep('Node_bash'),
'union':union}
def pp(x,y):
    return x


def load():
    global masters,codes
    codes=[]
    for i in os.listdir(root +'/codes/'):
        text=open(root +'/codes/'+i,'r').read()
        link='/codes/'+i
        codes.append((i,text,link))
    masters=[]
    def eval_secure(x):
        try:
            return eval(x,NODES)
        except Exception as error:
            return {'Compile_error':'''<div style="background-color:red" >{} </div>'''.format(error)}
    for i in os.listdir(root +'/masters/'):
        text=open(root +'/masters/'+i,'r').read()
        try:
            aux = eval(( 
                (subprocess.run(
                ['python3',os.path.dirname(os.path.abspath(__file__)),'-m',os.getcwd()+'/masters/'+i,'--md5'],
                
                check=True, stdout=subprocess.PIPE).stdout).decode("utf-8")),NODES)
            isinp=lambda x: int(x[:3]=='inp')
        except:
            print('i failed',i)
            aux={ 'fake':'dsafdsaf'}
            isinp=lambda x:2
        keys=sorted(map(
            lambda x:(x[0],
                'exec/{i}/{c}'.format(i=i,c=x[0]),
                x[1],
                (isinp((x[1]))),
            

           get_date(aux.get(x[0],'None')) ),eval_secure(text).items()) 
            
            ,key=lambda x:x[0]
                
            
            )

        link='/masters/'+i
        masters.append((i,text,link,keys,
            
            ))
load()

def gim(l,quiet_error=False):
    #eval the commnad "gim { l.split()}"
    comand=['python3',os.path.dirname(os.path.abspath(__file__)),
]+(l.split() if type(l)==str else list(l))
    print(*comand)
    s = (subprocess.run(comand,  check=not quiet_error, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE if quiet_error else None 
                    ))
    if not quiet_error:
        return '' if s.stdout is None else s.stdout.decode("utf-8")
    return ('' if s.stdout is None else s.stdout.decode("utf-8"),
            '' if s.stderr is None else s.stderr.decode('utf8'))


@app.route('/dot/<path:masters>',methods =['GET','POST'] )
def createdot(masters):
    code_dot = gim('-m {} -g -f dot'.format(masters),0)
    return render_template('dot_read.html',graph= code_dot.replace('\"','\\\"').replace('\n','').replace('digraph{','').replace('}',''))


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
            out=gim(['-m',os.getcwd()+'/masters/'+master,'-t',node,'--md5']).strip()
            nodes.append('<li>{}:({})>{}</li>'.format(node,master,out))
            out='.data/'+out
            File.save(out)
        return '''<h1>Updates:</h1>
        <ul>{}</ul>
        <a href='/'>back </a>'''.format(' '.join(nodes))

@app.route('/masterdoc/<master>')
def master(master):
    from __main__ import get_dot
    
    get_dot('/tmp/'+master+'.svg','svg',open('masters/'+master,'r').read(),False,None)
    return render_template('master.html',
            master=(open('/tmp/'+master+'.svg').read()))

#@app.route('/codes/<name>')
def code(name):
    name=root +'/codes/'+name
    text=open(name,'r').read()
    return render_template('code.html',
            file=name,
            text=text,
            path=name)

@app.route('/newmaster')
def newmaster():
    global masters,codes
    exists=set(os.listdir(os.getcwd()+'/masters'))
    file_base='new_master'
    file=file_base+'.py'
    i=1
    while file in exists:
        file=file_base+'('+str(i)+')'+'.py'
        i+=1

    f = open(os.path.join(os.getcwd(),'masters',file,), 'a')
    print('{}',file=f)
    f.close(
            )
    return redirect('/reload')

    
@app.route('/newcode')
def newcode():
    global masters,codes
    exists=set(os.path.join(os.getcwd(),'/code'))
    file_base='new_code'
    file=file_base+'.py'
    i=1
    while file in exists:
        file=file_base+'('+str(i)+')'+'.py'
        i+=1    
    f=open(os.path.join(os.getcwd(),'codes',file), 'a')
    print('{}',file=f)
    f.close()
    return redirect('/reload')


@app.route('/reload')
def reload():
    global masters,codes
    load()
    return redirect('/')

@app.route('/exec/<master>/<t>')
def execute(master,t):
    cmd = ['-m',os.getcwd()+'/masters/'+master,'-t',t,'-q']
    out,err=gim(cmd,True)
    if err:
        return """<pre><code><font color="red">{}</font></code></pre>""".format('\n'.join(err.split('\n')))
    #'''{}'''.format(exc.message if hasattr(exc,'message') else exc)
    out=out.split()
    if len(out)>1:
        return open(os.getcwd()+'/'+out[0],'r').read()
    out=os.getcwd()+'/'+out[0]
    return send_file(out ,attachment_filename=t[-1])

def run():
    app.run(debug=True)
############################
#####Here starts editor#####
############################
############################

def authenticate_password(password):
    hashed = hashlib.sha512(password.encode()).hexdigest()
    return hashed == config.passhash


def authenticate_key(key):
    if not config.passhash:
        return True
    if not key:
        return False
    if key == config.key:
        return True


def browse(path):
    File = namedtuple("File", "path_url name")
    dirs = []
    files = []
    parent, _ = os.path.split(path)

    for name in os.listdir(make_filepath(path)):
        path_url = "/" + os.path.join(path, name)
        f = File(path_url, name)
        if os.path.isdir(make_filepath(f.path_url[1:])):
            dirs.append(f)
        else:
            files.append(f)

    return render_template("browse.html",
                            path=path,
                            parent=parent,
                            dirs=sorted(dirs),
                            files=sorted(files))

def edit(path):
    with open(make_filepath(path), 'r') as f:
        content = f.read()
    return render_template("edit.html",
                            content=content,
                            path=make_filepath(path,'codes'))


def find_extension(path):
    i = path.rfind(".")
    return path[i:]


def make_filepath(path,folder=''):
    if folder:
        path = os.path.join(os.getcwd(),folder, path)
    else:
        path = os.path.join(os.getcwd(), path)
    print(path)
    return path

def view(path):
    if find_extension(path) == ".md":
        content = fh.get_html_from_md(make_filepath(path))
    else:
        with open(make_filepath(path), 'r') as f:
            content = "<pre><code>{}</code></pre>".format(f.read())
    
    parent_url, filename = os.path.split(path)
    parent_url = "/" + parent_url
    file_url = "/" + path
    return render_template("view.html",
                            content=content,
                            parent_url=parent_url,
                            file_url=file_url)


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        if not authenticate_password(request.form['password']):
            return render_template("authenticate.html")
        resp = make_response(render_template("authenticate.html"))
        resp.set_cookie('key', config.key)
        return resp
    return render_template("login.html")


@app.route("/ed", methods = ["GET", "POST"])
@app.route("/ed/<path:path>", methods = ["GET", "POST"])
def editor(path=""):
    path = '/'.join(path.split('/'))
    key = request.cookies.get('key')
    #if not authenticate_key(key):
    #    return render_template("login.html")

    filepath = make_filepath(path)

    # parse POST request, used for simple file commands
    if request.method == "POST":
        if request.form['command'] == "make_file":
            fh.make_file(filepath, request.form['name'])

        elif request.form['command'] == "make_dir":
            fh.make_dir(filepath, request.form['name'])

        elif request.form['command'] == "rename":
            fh.rename(filepath, request.form['new_name'])

        elif request.form['command'] == "save":
            fh.save(filepath, request.form['text'])

        elif request.form['command'] == "delete_dir":
            fh.delete_dir(filepath)

        elif request.form['command'] == "delete_file":
            fh.delete_file(filepath)

        else:
            return "could not understand POST request"
        return "done"

    # if directory then browse
    if os.path.isdir(filepath):
        return browse(path)

    # if not a directory and not a file then 404
    if not os.path.isfile(filepath):
        return filepath
        abort(404)

    # edit
    if "edit" in request.args:
        return edit(path)

    # view
    return view(path)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")



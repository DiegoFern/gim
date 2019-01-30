import subprocess    
from itertools import chain
from flask import Flask,render_template,flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import platform
from flask import send_file
import os
import sys 
import time


    

class run:
    def __init__(self,server):
        self.g=__import__(server)
        s=g.gim.gim
        self.dot=s.get_dot()

        self.app=app
        self.app.run()
    
    @app.route('/',methods =['GET','POST'] )
    def index(self):
        render_template(dot=self.dot,
                )


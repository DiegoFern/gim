from utils import *
from pprint import pprint
class dict_rec(dict):
    def __getitem__(self,b):
        bc=b
        cut=1
        while not b in self and cut>0:
            cut=b.find('.')
            b=b[cut+1:]
        if b:
            return dict.__getitem__(self,b)
        else:
            raise Exception('non found {}'.format(bc))
        
def import_node(master):
    return eval(open(master).read())
def  compile_master(text):
    G=eval(text)
    G=plain(G)
    return dict_rec(G)

def plain(G,header=''):
    G2={}
    for a,b in G.items():
        #assert '.' not in a, 'is forbbiden the use of "." nodes of master'
        if type(b)==dict:
            for c,d in plain(b,header=a+'.'+header).items():
                G2[a+'.'+c]=d
                d.update_inputs(header+a)
        else:
            G2[a]=b
    return G2

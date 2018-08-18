from utils import *
from pprint import pprint
def import_node(master):
    return eval(open(master).read())
def  compile_master(text):
    G=eval(text)
    G=plain(G)
    return G
class dict_with_levels(dict):
    def __getitem__(self,d):
        index=1
        dcopy=d
        while index>0:
            if d in  self:
                return dict.__getitem__(self,d)
            index=d.find('.')
            d=d[index+1:
                    ]
        raise Exception('Node not existent "{}"'.format(dcopy))
def plain(G,header=''):
    G2=dict_with_levels()
    for a,b in G.items():
        #assert '.' not in a, 'is forbbiden the use of "." nodes of master'
        if type(b)==dict:
            for c,d in plain(b,header=a+'.'+header).items():
                G2[a+'.'+c]=d
                d.update_inputs(header+a)
        else:
            G2[a]=b
    return G2

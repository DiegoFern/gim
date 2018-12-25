'''
python3 join.py A.csv B.csv a1 b1 a2 b2 ... an bn
if n==0 => makes natural join
'''
from collections import *
import csv
import sys
left=sys.argv[1]

rigth=sys.argv[2]
on =(sys.argv[3:])
on_left  = [o for i,o in enumerate(on) if i%2==0]
on_rigth = [o for i,o in enumerate(on) if i%2==1]
class CSV:
    def __init__(self,tabla,sep):
        self.tabla=list((csv.reader(open(sys.argv[1],'r'), 
            delimiter=';', lineterminator='\n')))
    def __iter__(self):
        return self.tabla[0].__iter__()
    def iterrows(self):
        return iter(self.tabla)

def get(a,l):
    return tuple(a[i] for i in l)

def merge(A,B,left_on=on_left,how='inner',right_on=on_rigth):
    assert len(left_on)==len(on_left)
    iterA=iter(A.iterrows())
    iterB=iter(B.iterrows())
    hA=next(iterA)
    hB=next(iterB)
    posA = [i for i,h in enumerate(hA) if h in left_on]
    posB = [i for i,h in enumerate(hB) if h in right_on]
    Da=defaultdict(list)
    Db=defaultdict(list)
    for i in iterA:
        Da[get(i,posA)].append(i)
    for i in iterB:
        Db[get(i,posB)].append(i)
    ans=[hA+hB]
    alt_A=alt_B=()
    if how=='left':
        alt_B=([None]*len(hB),)
    elif how=='rigth':
        alt_A=([None]*len(hA),)

    for index in set(Da).union(Db):
        for a in Da.get(index,alt_A):
            for b in Db.get(index,alt_B):
                ans.append(a+b)
    return CSV_list(ans)


class CSV_list:
    def __init__(self,list):
        self.list=list
    def to_csv(self):

        w=csv.writer(sys.stdout, delimiter=';', lineterminator='\n')
        for l in self.list:
            w.writerow(l)
A=CSV(left,sep=';')
B=CSV(rigth,sep=';')

if len(on_left)==0:
    on_left=on_rigth=list(set(A).union(set(B)))



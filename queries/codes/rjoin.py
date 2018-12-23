'''
python3 join.py A.csv B.csv a1 b1 a2 b2 ... an bn
if n==0 => makes natural join
'''
import csv
import sys
import pandas as pd
left=sys.argv[1]

rigth=sys.argv[2]
on =(sys.argv[3:])
on_left  = [o for i,o in enumerate(on) if i%2==0]
on_rigth = [o for i,o in enumerate(on) if i%2==1]
A=pd.read_csv(left,sep=';')
B=pd.read_csv(rigth,sep=';')
if len(on_left)==0:
    on_left=on_rigth=list(set(A).union(set(B)))
print(pd.merge(A,B,
                left_on=on_left,right_on=on_rigth).to_csv(sep=';',index=None,how='right'),end='')

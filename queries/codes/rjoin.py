'''
python3 join.py A.csv B.csv a1 b1 a2 b2 ... an bn
if n==0 => makes natural join
'''
HOW='rigth'
from base_join import *
(merge(A,B,
                left_on=on_left,right_on=on_rigth,how=HOW).to_csv(
            ))

import sys

l=0

for i in [sys.argv[1],sys.argv[2]]:
    for a in open(i,'r'):
        l+=int(a.strip())
if len(sys.argv)==4:
    print(l,file=open(sys.argv[3],'w'))
else:
    print(l)


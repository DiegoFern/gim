import sys

l=0

for i in sys.argv[1:]:
    for a in open(i,'r'):
        l+=int(a.strip())
print(l,)


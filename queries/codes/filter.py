import csv
import sys

It=iter(csv.reader(open(sys.argv[1],'r'), delimiter=';'))
l =next(It)
header = list(map(str,l))
w=csv.writer(sys.stdout, delimiter=';')

cond = ' '.join(sys.argv[2:])

w.writerow(l)
def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
for l in It:
    for h,v in zip(header,l):
        get_vars="{}={}".format(h,(v) if is_number(v) else repr(v))
        exec(get_vars)
    a= eval(cond)
    if a:
        w.writerow(l)

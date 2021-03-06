import os
def parse(argv):
    from optparse import OptionParser
    usageStr = """
    USAGE:     create_node -N name -o master/folder -n [Node|Node_bash] -f file
    -i imputs -a args[-d docs]  
    """
    parser = OptionParser(usageStr)
    #parser.add_option('-n', '--numGames', dest='numGames', type='int',
    #                  help=default('the number of GAMES to play'),
    #                  metavar='GAMES', default=v1)
    parser.add_option('-N','--name',dest='name',type=str,default=False,
            )

    parser.add_option('-o','--output',dest='output',type=str,default=None
            )
    parser.add_option('-n',dest='type',type=str,default='Node',
            help='output the log ')
    parser.add_option('-f',dest='file',type=str,default='[]',
            help='output the log ')
    parser.add_option('-i',dest='input',type=str,default='',
            help='output the log ')
    parser.add_option('-a',dest='args',type=str,default='',
            help='output the log ')
    parser.add_option('-c',dest='cmd',type=str,default='',
            help='output the log ')
    return parser.parse_args(argv)

def execute():
    import sys
    args=parse(sys.argv)[0]
    inp=(args.input).split(',') if len(args.input)>0 else []
    arg=(args.args).split(',') if len(args.args)>0 else ''
    for a in inp:
        
        assert all([os.path.isfile(args.output+'/'+a)]),args.output+'/'+a
    with open(args.output+'/'+args.name,'w') as f:
        print(args.type,end='(**',file=f)
        print({'inputs':((inp)),'File':args.file,
            'args':arg,'cmd':args.cmd,
            },file=f)
        print(')',file=f)

execute()

import argparse
def cmdline_parse():
    parser=argparse.ArgumentParser()

    target = parser.add_argument_group('TARGET')
    target.add_argument("-u",dest="url",help="Please input a url to dir")
    target.add_argument("-l",dest="list",help="A list to scan")
    
    target.add_argument("-spider",dest="spider",help="A spider to scan")
    target.add_argument("-deep",dest="deepth",type=int,default=2,help="The deepth of spider")

    api = parser.add_argument_group('API')
    api.add_argument("-zoomeye",dest="zoomeye",help="the api for zoomeye")
    api.add_argument("-b",dest="baidu",help="the word of baidu search")
    api.add_argument("-ln",dest="limitnum",type=int,default=10,help="the target number you need")

    engine=parser.add_argument_group("ENGINE")
    engine.add_argument("-t",dest="thread",help="the num of thread")
    engine.add_argument("-m",dest="mode",help="The mode of urltest")

    script=parser.add_argument_group("SCRIPT")
    script.add_argument('-f',dest='finger',help="CMS Scan")
    script.add_argument("-s",dest="script",help="the script to use")
    script.add_argument("-ss",dest="showscript",help="to show all the scripts")


    args=parser.parse_args()
    return args

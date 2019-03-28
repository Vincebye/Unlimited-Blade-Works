import argparse
def cmdline_parse():
    parser=argparse.ArgumentParser()
    parser.add_argument("-u",dest="url",help="Please input a url to dir")
    parser.add_argument("-l",dest="list",help="A list to scan")
    parser.add_argument("-api",dest="api",help="zoomeye")
    parser.add_argument("-t",dest="thread",help="the num of thread")
    parser.add_argument("-s",dest="script",help="the script to use")
    parser.add_argument("-m",dest="mode",help="The mode of urltest")
    parser.add_argument("-zoomeye",dest="zoomeye",help="the api for zoomeye")
    parser.add_argument("-ln",dest="limitnum",help="the number you need")
    parser.add_argument("-kw",dest="keyword",help="the keyword you search")

    args=parser.parse_args()
    return args

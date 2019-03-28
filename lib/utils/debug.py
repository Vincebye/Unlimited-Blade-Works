def str2ascii(string1):
    for i in string1:
        print(ord(i))
def compare(string1,string2):
    if string1==string2:
        print('====')
    elif string1>string2:
        print(str2ascii(string1))
        print('>>>>>')
        print(str2ascii(string2))
    elif string1<string2:
        print(str2ascii(string1))
        print('<<<<<<')
        print(str2ascii(string2))
    else:
        print(string1)
        print(string2)

def debug_print(string1):
    print('\n*******************')
    print(string1)
    print('\n*******************')

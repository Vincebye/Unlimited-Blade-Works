import os
test=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
def poc(target):
    print(target)
    print('\n')
    print('success')
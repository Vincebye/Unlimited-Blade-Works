from lib.core.data import paths
import os
def set_paths():
    root_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    paths.root=root_path
    paths.script=root_path+'/script'

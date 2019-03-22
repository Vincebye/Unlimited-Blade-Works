from lib.core.data import *
from lib.core.gather import get_targets
from lib.core.survey import header_probe
import importlib
def load_module():
    script_name='script.'+conf.script
    realman.obj=importlib.import_module(script_name)

def load_payload():
    get_targets()
    

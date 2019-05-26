from lib.core.data import *
from lib.core.gather import get_targets
import importlib
from lib.core.survey import whatcms
from lib.core.log import ConsoleLogger
from lib.core.enums import LOGGING_MESSAGE
def load_module():
    if conf.script:
        script_name='script.'+conf.script
        ConsoleLogger.Warning(LOGGING_MESSAGE.LOADER_POC_MESSAGE.format(poc=conf.script))

        realman.obj=importlib.import_module(script_name)


def load_payload():
    ConsoleLogger.Warning(LOGGING_MESSAGE.LOADER_CMS_MESSAGE)
    if conf.finger:
        whatcms()
    ConsoleLogger.Warning(LOGGING_MESSAGE.LOADER_GATHER_MESSAGE)

    get_targets()

    # url=realman.queue.get()
    # header_probe(url)
    # print(realman.timo)

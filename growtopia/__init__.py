from .parsers import *
from .utils import *

if not Logger.running and not Logger.start():
    print(AnsiStr("Failed to start logger").wrap(AnsiESC.RED))

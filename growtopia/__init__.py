from .parsers import *
from .utils import *

if not Logger._running and not Logger.start():
    print(AnsiStr("Failed to start logger").wrap(AnsiESC.RED))

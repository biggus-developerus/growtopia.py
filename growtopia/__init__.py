from .parsers import *
from .utils import *

if not Logger.start():
    print(AnsiStr("Failed to start logger").wrap(AnsiESC.RED))
else:
    log_info("Logger started")

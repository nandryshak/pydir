from time import gmtime
from sys import exit

'''
Monty's Debug Library. Copyright Nicolas "Montessquio" Suarez 2018.
Designed for use as a python import and should not be executed explicitly.
'''

# Debugger class.
class logger:
    # Logging levels.
    # -1 = Disabled. 0 = INFO, 1 = WARN, 2 = ERROR, 3 = Internal Logs. FATAL will trigger at all levels aside from -1.
    def __init__(self, level=0):
        self.level = level
        self.log("Console Logging Initialised")

    # Standard Logging level (1)
    def log(self, msg):
        if(self.level >= 0):
            print("[INFO][" + ftime() + "] " + msg)

    # More serious logging level (2)
    def warn(self, msg):
        if(self.level >= 1):
            print("[WARN][" + ftime() + "] " + msg)

    # Most serious recoverable logging level (3)
    def error(self, msg):
        if(self.level >= 2):
            print("[ERROR][" + ftime() + "] " + msg)

    # Exits after
    def fatal(self, msg):
        if(self.level >=0):
            print("[FATAL][" + ftime() + "] " + msg)
            exit()

    # fatals(afe) does not exit after giving a message.
    # should not be used. Instead, see error.
    def fatals(self, msg):
        if(self.level >= 0):
            print("[FATAL][" + ftime() + "] " + msg)
            print("Continuing...")

    # internal logger. This should be used by modules only.
    def ilog(self, calling_module, msg):
        pass #Stub

# Internal Functions
# Internal function for getting the current time string (formatted)
# Format is HH:MM:SS
def ftime():
    return ':'.join([str(gmtime().tm_hour), str(gmtime().tm_min), str(gmtime().tm_sec)])

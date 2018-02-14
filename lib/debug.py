from time import gmtime
from sys import exit
from json import dumps
from os import path
import json

'''
Monty's Debug Library. Please note this software may be licenced differently
than the software that uses it.
Designed for use as a python import and should not be executed explicitly.

Copyright (C) 2018 Nicolas "Montessquio" Suarez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

# Debugger class.
class logger:
    # Logging levels.
    # -1 = Disabled. 0 = INFO, 1 = WARN, 2 = ERROR, 3 = Internal Logs. FATAL will trigger at all levels aside from -1.
    # Manually set doIL to log ILOGS without changing overall log level. Basically -v flag.
    def __init__(self, level=0, doIL = False, quiet=False, oFile = None):
        self.level = level
        self.doIL = doIL
        self.quiet = quiet

        try: self.oFile = path.abspath(oFile)
        except: self.oFile = None

    # Standard Logging level (1)
    def log(self, msg, endl="\n"):
        if((self.level >= 0) and (self.quiet == False)):
            try:
                print("[INFO][" + __ftime__() + "] " + msg, end=endl)
            except:
                print("[INFO][" + __ftime__() + "] " + dumps(msg), end=endl)

        if( self.oFile != None ):
            try:
                with open(self.oFile, "a") as f:
                    try:
                        f.write("[INFO][" + __ftime__() + "] " + msg + endl)
                    except:
                        f.write("[INFO][" + __ftime__() + "] " + dumps(msg) + endl)
            except Exception as e:
                print("[ERROR][" + __ftime__() + "] Unable to write to log file. Error : " + json.dumps(e), end=endl)

    # More serious logging level (2)
    def warn(self, msg, endl="\n"):
        if(self.level >= 1):
            try:
                print("[WARN][" + __ftime__() + "] " + msg, end=endl)
            except:
                print("[WARN][" + __ftime__() + "] " + dumps(msg), end=endl)

        if( self.oFile != None ):
            try:
                with open(self.oFile, "a") as f:
                    try:
                        f.write("[INFO][" + __ftime__() + "] " + msg + endl)
                    except:
                        f.write("[INFO][" + __ftime__() + "] " + dumps(msg) + endl)
            except:
                print("[ERROR][" + __ftime__() + "] Unable to write to log file.", end=endl)

    # Most serious recoverable logging level (3)
    def error(self, msg, endl="\n"):
        if(self.level >= 2):
            try:
                print("[ERROR][" + __ftime__() + "] " + msg, end=endl)
            except:
                print("[ERROR][" + __ftime__() + "] " + dumps(msg), end=endl)

        if(self.self.oFile != ""):
            try:
                with open(self.self.oFile, "w") as f:
                    try:
                        f.write("[INFO][" + __ftime__() + "] " + msg + endl)
                    except:
                        f.write("[INFO][" + __ftime__() + "] " + dumps(msg) + endl)
            except:
                print("[ERROR][" + __ftime__() + "] Unable to write to log file.", end=endl)

    # Exits after execution. Optional cleanup method.
    def fatal(self, msg, methodCleanup = "", endl="\n"):
        if(self.level >=0):
            try:
                print("[FATAL][" + __ftime__() + "] " + msg, end=endl)
            except:
                print("[FATAL][" + __ftime__() + "] " + dumps(msg), end=endl)

        if( self.oFile != None ):
            try:
                with open(self.oFile, "a") as f:
                    try:
                        f.write("[INFO][" + __ftime__() + "] " + msg + endl)
                    except:
                        f.write("[INFO][" + __ftime__() + "] " + dumps(msg) + endl)
            except:
                print("[ERROR][" + __ftime__() + "] Unable to write to log file.", end=endl)

        try: exec(methodCleanup) # This should not be here, use something else.
        except: pass
        exit()

    # fatals(afe) does not exit after giving a message.
    # should not be used. Instead, see error.
    def fatals(self, msg, endl="\n"):
        if(self.level >= 0):
            try:
                print("[FATAL][" + __ftime__() + "] " + msg, end=endl)
            except:
                print("[FATAL][" + __ftime__() + "] " + dumps(msg), end=endl)

        if( self.oFile != None ):
            try:
                with open(self.oFile, "a") as f:
                    try:
                        f.write("[INFO][" + __ftime__() + "] " + msg + endl)
                    except:
                        f.write("[INFO][" + __ftime__() + "] " + dumps(msg) + endl)
            except:
                print("[ERROR][" + __ftime__() + "] Unable to write to log file.", end=endl)

        print("Continuing...")

    # internal logger.
    def ilog(self, msg, endl="\n"):
        if((self.level >= 3) or (self.doIL == True)):
            try:
                print("[iLog][" + __ftime__() + "] " + msg, end=endl)
            except:
                print("[iLog][" + __ftime__() + "] " + dumps(msg), end=endl)

            if( self.oFile != None ):
                try:
                    with open(self.oFile, "a") as f:
                        try:
                            f.write("[INFO][" + __ftime__() + "] " + msg)
                        except:
                            f.write("[INFO][" + __ftime__() + "] " + dumps(msg))
                except:
                    print("[ERROR][" + __ftime__() + "] Unable to write to log file.", end=endl)

# Internal Functions
# Internal function for getting the current time string (formatted)
# Format is HH:MM:SS
def __ftime__():
    return ':'.join([str(gmtime().tm_hour), str(gmtime().tm_min), str(gmtime().tm_sec)])

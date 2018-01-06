#vvv# Don't Touch These #vvv#'''
import sys
import lib.debug as debug


#vvv# General Config #vvv#'''
_EXCLUDES = ["lib", "app.py", "rsc"] # Exclude matching files or folders from program operation
#_ROOTDIR = "Manually Specify Root working Directory. Not reccomended for use."
_DIRFILENAME = "directory.html" # What should the directory html file be called?

#vvv# Unless you want to debug the program leave this at the default. #vvv#'''
_LOGLEVEL = 0 # Console debug log level. -1 for none, 0 for info, 1 for warning, 2 for errors, 3 for verbose.

#vvv# These should generally not be modified unless you know what you're doing. #vvv#'''
_ITEMTEMPLATE = open("rsc/item-template.html").read() # What HTML to duplicate and fill for each file/dir
_THEME = open("rsc/theme.html").read() # This is the html that should enclose the $content$
_STYLESHEET = open("rsc/stylesheet.html").read() # This stylesheet will be placed in the <head> section of the final HTML

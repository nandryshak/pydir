#vvv# Don't Touch These #vvv#'''
import sys
import lib.debug as debug


#vvv# General Config #vvv#'''
_EXCLUDES = [
    "lib",
    "app.py",
    "rsc",
    ".git",
    "include",
    "index.html",
    "directory.html",
    "search.html",
    ".git",
    "__pycache__",
    "dir.idx"
] # Exclude matching files or folders from program operation
#_ROOTDIR = "Manually Specify Root working Directory. Not reccomended for use."
_DIRFILENAME = "index.html" # What should the directory html file be called?
_DOMAIN = "localhost" # Set this to your domain name.
_ALPHAORDER = True # Change to False if you do not want files and folders to be sorted alphabetically ( folders will still appear above files )

_FOLLOWSYMLINKS = True      # Should the spider follow symbolic links?
_ALLOW_OUT_OF_WEBROOT = False # When false, this will restrict symlink destinations to only those within the _WEBROOT
_WEBROOT = "/var/www/html"   # THIS MUST BE CHANGED FOR SYMLINKS TO WORK.

_SKIPDIRS = False   # Should directories with no changes made since last run be skipped?
                    # Turn this off if pages aren't all updating properly.

#vvv# Unless you want to debug the program leave this at the default. #vvv#'''
_LOGLEVEL = 2 # Console debug log level. -1 for none, 0 for info, 1 for warning, 2 for errors, 3 for verbose.

#vvv# These should generally not be modified unless you know what you're doing. #vvv#'''
_ITEMTEMPLATE = open("rsc/item-template.html").read() # What HTML to duplicate and fill for each file/dir
_THEME = open("rsc/theme.html").read() # This is the html that should enclose the $content$

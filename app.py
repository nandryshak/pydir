# Python Builtins
import sys
import os
from json import dumps

# Custom Modules (found in ./lib )
import lib.debug as debug
#import lib.format

# Set up runtime variables.
_EXCLUDES = ["lib", "app.py", "rsc"] # Exclude certain files or folders from program operation
_ROOTDIR = sys.argv[1] # The root working directory is specified as a cli arg.
_DIRFILENAME = "directory.html" # What should the directory html file be called?
console = debug.logger(level=0) # What kinds of messages to log. See logging module for more info.

_ITEMTEMPLATE = open("rsc/item-template.html").read() # What HTML to duplicate and fill for each file/dir
_DIRHEADER = open("rsc/dir-header.html").read() # This is the html that should contain css styles.
_DIRFOOTER = open("rsc/dir-footer.html").read() # This is the html that should contain js script references.


# Misc Utilities
def stub():
    pass

# MAIN PROGRAM
os.chdir(_ROOTDIR) # Switch to specified working directory.

# Get directory tree based on first argument
for root, dirs, files in os.walk("."):

    # In every root directory, create a directory.html file.
    try:
        dirFile = open(root + ("/"+_DIRFILENAME), "w")
    except OSError: console.error("Could not create directory.html for root " + root)

    # Remove the _EXCLUDES from traversal targets
    for item in _EXCLUDES:
        try:
            dirs.remove(item)
        except:
            try:
                files.remove(item)
            except:
                console.warn("Exclude " + item + " not found in \"" + root + "\" ... Moving on...")
    # Also remove .html files.
    for item in files:
        if item.endswith(".html"):
            files.remove(item)

    # Now traverse files and folders in the current root and add them, through the template, to directory.html
    fileText = "" # Begin with an empty string.

    # Add the "../" directory.
    tmp = _ITEMTEMPLATE.replace("$class$", 'icon up') # icon-type is up (dir up)
    tmp = tmp.replace("$file-href$", ("../"))
    tmp = tmp.replace("$filename$", "Parent Directory")
    fileText += tmp
    fileText += "\n"

    for item in dirs: # First add the dirs
        tmp = _ITEMTEMPLATE.replace("$class$", 'icon dir') # icon-type is dir.
        tmp = tmp.replace("$file-href$", ("." + "/" + item)) # subdirs are in "this" dir so it can be ./<file>
        tmp = tmp.replace("$filename$", item)
        fileText += tmp
        fileText += "\n"
    for item in files: # Second add the files
        tmp = _ITEMTEMPLATE.replace("$class$", 'icon file') # icon-type is file.
        tmp = tmp.replace("$file-href$", ("." + "/" + item)) # files are in "this" dir so it can be ./<file>
        tmp = tmp.replace("$filename$", item)
        fileText += tmp
        fileText += "\n"

    dirFile.write(_DIRHEADER + '\n<h1 class="title">Index of /' + root.strip("./") + '</h1>' + fileText + _DIRFOOTER)

console.log("Done.")

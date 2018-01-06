# Python Builtins
import sys
import os
from json import dumps
from time import clock

# Custom Modules (found in ./lib )
import lib.debug as debug
#import lib.format

# Set up runtime variables.
_EXCLUDES = ["lib", "app.py", "rsc"] # Exclude certain files or folders from program operation
_ROOTDIR = sys.argv[1] # The root working directory is specified as a cli arg.
_DIRFILENAME = "directory.html" # What should the directory html file be called?
console = debug.logger(level=0) # What kinds of messages to log. See logging module for more info.

_ITEMTEMPLATE = open("rsc/item-template.html").read() # What HTML to duplicate and fill for each file/dir
_THEME = open("rsc/theme.html").read() # This is the html that should enclose the $content$


# Misc Utilities
def stub():
    pass

# MAIN PROGRAM
os.chdir(_ROOTDIR) # Switch to specified working directory.
console.log("Working directory is now " + _ROOTDIR)

# Get directory tree based on first argument
console.log("Beginning directory traversal...")
__STARTTIME__ = clock()
for root, dirs, files in os.walk("."):
    __DIRSTARTTIME__ = clock()
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
    fileCount = 0 # Keep track of how many entries are in this particular directory.
    dirCount = 0

    # Add the "../" directory.
    tmp = _ITEMTEMPLATE.replace("$class$", 'icon') # icon-type is up (dir up)
    tmp = tmp.replace("$item-type$", 'icon up-icon')
    tmp = tmp.replace("$file-href$", "../")
    tmp = tmp.replace("$filename$", "Parent Directory")
    fileText += tmp
    fileText += "\n"

    for item in dirs: # First add the dirs
        tmp = _ITEMTEMPLATE.replace("$class$", 'icon')
        tmp = tmp.replace("$item-type$", 'icon dir-icon')# icon-type is dir.
        tmp = tmp.replace("$file-href$", ("." + "/" + item)) # subdirs are in "this" dir so it can be ./<file>
        tmp = tmp.replace("$filename$", item)
        fileText += tmp
        fileText += "\n"
        dirCount += 1

    for item in files: # Second add the files
        tmp = _ITEMTEMPLATE.replace("$class$", 'icon file')
        tmp = tmp.replace("$item-type$", 'icon file-icon') # icon-type is file.
        tmp = tmp.replace("$file-href$", ("." + "/" + item)) # files are in "this" dir so it can be ./<file>
        tmp = tmp.replace("$filename$", item)
        fileText += tmp
        fileText += "\n"
        fileCount += 1

    fileText = _THEME.replace("$content$", fileText) # Insert the generated page-content into the theme.

    # Theme Variable Insertion here
    fileText = fileText.replace("$root-dir$", '<h1 class="title">Index of /' + root.strip("./") + '</h1>')

    # Write the composed HTML to a file.
    dirFile.write(fileText)
    console.log("Generated " + str(dirCount) + " directories and " + str(fileCount) + " files in folder /" + root.strip("./") + ". Took " + str(round(((clock() - __DIRSTARTTIME__)*1000), 3)) + "ms")

console.log("Done. Took " + str(round(((clock() - __STARTTIME__)*1000), 3)) + "ms")

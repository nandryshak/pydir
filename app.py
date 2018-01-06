"""
##########################################
PYDir - Generate beautiful static directory listings for your site.

Edit rsc/theme.html to modify the overall site structure.
The file rsc/stylesheet.html will be automatically added into the $stylesheet$ portion of the theme.html text.
rsc/item-template.html will be cloned and filled once per item in the directory, including `../` directories.
See rsc/stylesheet.html for the default css classes used in generation.
##########################################
"""

# Python Builtins
import os
import sys
from json import dumps
from time import clock

# Custom Modules (found in ./lib )
import lib.debug as debug

''' Set up runtime variables and configuration values. '''
_ROOTDIR = sys.argv[1] # The root working directory is specified as the first cli arg.
import cfg # Import the config file
console = debug.logger(level=cfg._LOGLEVEL) # Init log level before anything essential happens.

# Handle in case cfg.py does not contain cfg._ROOTDIR
try: _ROOTDIR = cfg._ROOTDIR
except: pass

# Assign the CFG Vars locally.
console.log("Assigning config values from `cfg.py` locally.")
_EXCLUDES = cfg._EXCLUDES # Exclude matching files or folders from program operation
_DIRFILENAME = cfg._DIRFILENAME # What should the directory html file be called?

_ITEMTEMPLATE = cfg._ITEMTEMPLATE # What HTML to duplicate and fill for each file/dir
_THEME = cfg._THEME # This is the html that should enclose the $content$
_STYLESHEET = cfg._STYLESHEET # This stylesheet will be placed in the <head> section of the final HTML
console.log("Done")

# Misc Utilities
def stub():
    pass

'''# MAIN PROGRAM START #'''
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
    fileText = fileText.replace("$root-dir$", root.strip("./"))
    fileText = fileText.replace("$stylesheet$", _STYLESHEET)

    # Write the composed HTML to a file.
    dirFile.write(fileText)
    console.log("Generated " + str(dirCount) + " directories and " + str(fileCount) + " files in folder /" + root.strip("./") + ". Took " + str(round(((clock() - __DIRSTARTTIME__)*1000), 3)) + "ms")

console.log("Done. Took " + str(round(((clock() - __STARTTIME__)*1000), 3)) + "ms")

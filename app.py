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
# from json import dumps # Mostly used for debugging
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
_EXCLUDES = cfg._EXCLUDES # Exclude matching files or folders from program operation
_DIRFILENAME = cfg._DIRFILENAME # What should the directory html file be called?
_DOMAIN = cfg._DOMAIN
_ITEMTEMPLATE = cfg._ITEMTEMPLATE # What HTML to duplicate and fill for each file/dir
_THEME = cfg._THEME # This is the html that should enclose the $content$
_STYLESHEET = cfg._STYLESHEET # This stylesheet will be placed in the <head> section of the final HTML
_ALPHAORDER = cfg._ALPHAORDER


'''# MAIN PROGRAM START #'''

console.log("Copying ./include to " + _ROOTDIR + "include")
os.system("cp -r include/ " + _ROOTDIR)

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
                pass
                #console.warn("Exclude " + item + " not found in \"" + root + "\" ... Moving on...")
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
    tmp = tmp.replace("$filesize$", "")
    fileText += tmp
    fileText += "\n"

    # Sort the files and folders into alphabetical order if the option is enabled.
    if _ALPHAORDER:
        dirs.sort()
    for item in dirs: # First add the dirs
        tmp = _ITEMTEMPLATE.replace("$class$", 'icon')
        tmp = tmp.replace("$item-type$", 'icon dir-icon')# icon-type is dir.
        tmp = tmp.replace("$file-href$", ("." + "/" + item)) # subdirs are in "this" dir so it can be ./<file>
        tmp = tmp.replace("$filename$", item)
        tmp = tmp.replace("$filesize$", "")
        fileText += tmp
        fileText += "\n"
        dirCount += 1

    if _ALPHAORDER:
        files.sort()
    for item in files: # Second add the files
        tmp = _ITEMTEMPLATE.replace("$class$", 'icon file')
        tmp = tmp.replace("$item-type$", 'icon file-icon') # icon-type is file.
        tmp = tmp.replace("$file-href$", ("." + "/" + item)) # files are in "this" dir so it can be ./<file>
        tmp = tmp.replace("$filename$", item)

        # Handle Filesizes
        try: # Preferred method, as it is very fast.
            fileSize = int(os.popen("du -b " + '"' + root + "/" + item + '"').read().split("\t")[0])
        except: # Failure likely means DU is not installed on the system, therefore we should use the slow method.
            console.warn("DU is either not installed or erroring. It is reccomended to have DU installed on your system; the backup method is very slow.")
            fileSize = len(open(root + "/" + item, "rb").read()) #File size is the length of all the bytes of the file. SLOW

        if fileSize >= 1000000000000: # More than a trillion bytes means it's in terabytes.
            fileSize = round((fileSize / 1000000000000), 2) # convert to terabytes
            fileSize = str(fileSize) + "TB"
        elif fileSize >= 1000000000: # More than a billion means it's in gigabytes.
            fileSize = round((fileSize / 1000000000), 2) # convert to gigabytes
            fileSize = str(fileSize) + "GB"
        elif fileSize >= 1000000: # More than a million means it's in megabytes.
            fileSize = round((fileSize / 1000000), 2) # convert to megabytes
            fileSize = str(fileSize) + "MB"
        elif fileSize >= 1000: # More than a thousand means it's in kilobytes.
            fileSize = round((fileSize / 1000), 2) # convert to kb
            fileSize = str(fileSize) + "KB"
        else: #Anything below is in bytes.
            fileSize = str(fileSize) + "B"

        # Add in the converted statistic
        tmp = tmp.replace("$filesize$", str(fileSize))


        fileText += tmp
        fileText += "\n"
        fileCount += 1

    fileText = _THEME.replace("$content$", fileText) # Insert the generated page-content into the theme.

    # Theme Variable Insertion here
    fileText = fileText.replace("$root-dir$", root.strip("./"))
    fileText = fileText.replace("$stylesheet$", _STYLESHEET)
    fileText = fileText.replace("$domain$", _DOMAIN)

    # => Handle the Breadcrumbs
    path = root.split("/")
    breadCrumb = ""
    crumbItem = '<a href="$addr$">$name$/</a> '


    for crumb in path:
        if crumb == ".":
            breadCrumb += crumbItem.replace("$name$", _DOMAIN)
        else:
            breadCrumb += crumbItem.replace("$name$", crumb.strip("./"))

        if path == ["."]:
            crumbAddr = '#'
        else:
            crumbAddr = ('../' * (len(path)-(path.index(crumb)+1)))
            crumbAddr += './'
        breadCrumb = breadCrumb.replace("$addr$", crumbAddr)

    fileText = fileText.replace("$breadcrumb$", breadCrumb) # write composed breadcrumb to file.

    # Write the composed HTML to a file.
    dirFile.write("")
    dirFile.write(fileText)
    console.log("Generated entries for " + str(dirCount) + " directories and " + str(fileCount) + " files in folder /" + root.strip("./") + ". Took " + str(round(((clock() - __DIRSTARTTIME__)*1000), 3)) + "ms")
    # print(fileText)
console.log("Done. Took " + str(round(((clock() - __STARTTIME__)*1000), 3)) + "ms")

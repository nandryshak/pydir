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
import json # Mostly used for debugging
from time import clock
from datetime import datetime
import tempfile # Used as a buffer zone for some functions
import random

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
_ALPHAORDER = cfg._ALPHAORDER

# Misc utils

# Thanks to https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
'''
def dirtree(startpath):
    l = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        for item in _EXCLUDES:
            try:
                dirs.remove(item)
            except:
                try:
                    files.remove(item)
                except:
                    pass
        if root not in _EXCLUDES:
            l.append((os.path.basename(root), level))
            return(l)
'''


# Recursive directory tree to JSON converter with excludes support.
# Modified version of https://unix.stackexchange.com/questions/164602/how-to-output-the-directory-structure-to-json-format
def dirTree(path, indent = 0, streak=0): # When called with no workingString argument(as it should be, it will start from scratch.)
    #_template = '''
    #<li class="pure-menu-item">
    #    <div class="side-checkbox">
    #        <input type="checkbox" id="collapse"/>
    #        <label class="list-collapsed-icon" for="collapse"></label>
    #    </div>
    #    <div class="side-content" id="a1">
    #        <a href="$side-href$" class="pure-menu-link">
    #            $side-name$
    #        </a>
    #    </div>
    #</li>
    #            '''
    for p in os.listdir(path):
        if p not in _EXCLUDES: # Make sure we're not looking at an ILLEGAL FOLDER >:(
            fullpath = os.path.join(path, p)
            if os.path.isdir(fullpath):
                uid = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for i in range(6))
                # Handle some css magic for the dropdowns.
                # Not the nicest thing but it works.
                # I need to dynamically write styles here to make use of the button hack
                tfile.write('<li class="pure-menu-item" style="padding-left: ' + str(indent * 10) + 'px"><div class="side-checkbox"><input type="checkbox" onclick="dropdown(this)" id="collapse_' + uid + '"/><label class="list-collapsed-icon" for="collapse_' + uid + '" id="chevron_' + uid + '"></label></div><div class="side-content" id="a1"><a href="$root-step$/' + str(fullpath) + '" class="pure-menu-link">' + str(p) + "</a></div>")
                tfile.write('<ul class="pure-menu-list default-hidden" id="' + uid + '">')
                dirTree(fullpath, indent=indent+1, streak=streak+1)
                tfile.write("</ul>")
            tfile.write("</li>")

# Convert byte count to size string
def fileSizeCount(fileSize):
    if fileSize >= 1000000000000: # More than a trillion bytes means it's in terabytes.
        fileSize = round((fileSize / 1000000000000), 2) # convert to terabytes
        fileSize = str(fileSize) + " TB"
    elif fileSize >= 1000000000: # More than a billion means it's in gigabytes.
        fileSize = round((fileSize / 1000000000), 2) # convert to gigabytes
        fileSize = str(fileSize) + " GB"
    elif fileSize >= 1000000: # More than a million means it's in megabytes.
        fileSize = round((fileSize / 1000000), 2) # convert to megabytes
        fileSize = str(fileSize) + " MB"
    elif fileSize >= 1000: # More than a thousand means it's in kilobytes.
        fileSize = round((fileSize / 1000), 2) # convert to kb
        fileSize = str(fileSize) + " KB"
    else: #Anything below is in bytes.
        fileSize = str(fileSize) + " B"
    return fileSize

# Get the size of a given file or folder.
def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


'''# MAIN PROGRAM START #'''

console.log("Copying ./include to " + _ROOTDIR + "/include")
os.system("cp -r include/ " + _ROOTDIR)

console.log("Copying ./search.html to " + _ROOTDIR)
SearchText = ""
with open('./rsc/search.html', 'r') as search_HTML: # First grab the original HTML template.
    SearchText = search_HTML.read().replace('$domain$', _DOMAIN) # Sub-in necessary values

os.chdir(_ROOTDIR) # Switch to specified working directory.
console.log("Working directory is now " + _ROOTDIR)

# Build the dirtree into an HTML object.
try:
    __DIRSTARTTIME__ = clock() # TIme the operation

    # All this is old stuff from the JSON-based generation. Now we do in-house HTML generation, and sub in the links using
    # the current root-step

    #_DIRTREE = dirTree(".")
    #_DIRSTRING = json.dumps(_DIRTREE).replace('\x00', '').replace(" null,", '').replace(' null', '').replace("null,", '')
    #with open('include/tree.json', 'w') as jsonFile:  # Write directory tree information in the include folder as tree.json
    #    jsonFile.write(json.dumps(_DIRTREE).replace('\x00', '').replace(" null,", '').replace(' null', '').replace("null,", ''))

    # dirTree exports it's composed HTML to a temporary file in memory.
    tfile = tempfile.SpooledTemporaryFile(mode="w+s")
    dirTree(".")
    tfile.seek(0)
    _DIRTREE = tfile.read()#[len('<ul class="pure-menu-list>')+1:] # Remove initial and final ul elements - they are already in the template
    #_DIRTREE = _DIRTREE[:-(len('</ul>'))]
    #print(_DIRTREE)
    console.log("Completed directory tree JSON generation in " + str(round(((clock() - __DIRSTARTTIME__)*1000), 3)) + "ms")
except Exception as e:
    console.warn("Could not complete directory tree JSON generation due to an unknown error. Substituting an empty dictionary instead.")
    console.warn("Error Information: " + str(e))
    _DIRTREE = ""

with open(_ROOTDIR + '/search.html', 'w+') as search_HTML_final: # Then write the composed HTML to file.
    search_HTML_final.write(SearchText.replace("$sidenav$", _DIRTREE))

# Reserve a global variable to contain a list of all files.
# Really it is an array of Dictionaries, where each dictionary is a single file
_files = []

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


    # Calculate the root-step
    rootStep = "."
    for item in root.split("/")[1:]:
        rootStep += "/.."

    # Now traverse files and folders in the current root and add them, through the template, to directory.html
    fileText = "" # Begin with an empty string.
    fileCount = 0 # Keep track of how many entries are in this particular directory.
    dirCount = 0

    # Add the "../" directory.
    tmp = _ITEMTEMPLATE.replace("$class$", 'icon no-sort') # icon-type is up (dir up)
    tmp = tmp.replace("$item-type$", 'icon up-icon')
    tmp = tmp.replace("$file-href$", "../")
    tmp = tmp.replace("$filename$", "Parent Directory")
    tmp = tmp.replace("$filesize$", "")
    tmp = tmp.replace("$last-modified$", "")
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

        # Handle Filesizes
        try: # Preferred method, as it is very fast.
            #fileSize = int(os.popen("du -bcks " + '"' + root + "/" + item + '"').read().split("\t")[0])
            fileSize = get_size(root + "/" + item)
            fileSize = fileSizeCount(fileSize)
        except: # Failure likely means DU is not installed on the system, therefore we should use the slow method.
            console.warn("DU is either not installed or erroring. It is reccomended to have DU installed on your system; the backup method is very slow.")
            console.warn("Folder size is not supported without DU")
            fileSize = ""

        # Add in the converted statistic
        tmp = tmp.replace("$filesize$", str(fileSize))

        tmp = tmp.replace("$last-modified$", datetime.fromtimestamp( int( os.path.getmtime(root+"/"+item) ) ).strftime('%Y-%m-%d %H:%M:%S'))

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
        tmp = tmp.replace("$last-modified$", datetime.fromtimestamp( int( os.path.getmtime(root+"/"+item) ) ).strftime('%Y-%m-%d %H:%M:%S'))

        # Handle Filesizes
        try: # Preferred method, as it is very fast.
            fileSize = int(os.popen("du -b " + '"' + root + "/" + item + '"').read().split("\t")[0])
        except Exception as e: # Failure likely means DU is not installed on the system, therefore we should use the slow method.
            console.warn("DU is either not installed or erroring. It is reccomended to have DU installed on your system; the backup method is very slow.")
            console.warn("Exception in file: " + root + "/" + item + " Is error :    " + str(e))
            fileSize = len(open(root + "/" + item, "rb").read()) #File size is the length of all the bytes of the file. SLOW

        fileSize = fileSizeCount(fileSize)

        # Add in the converted statistic
        tmp = tmp.replace("$filesize$", str(fileSize))


        fileText += tmp
        fileText += "\n"
        fileCount += 1

        # Add all the files into an array of dictionaries.
        fRecord = {'name': item}
        fRecord['size'] = fileSize
        fRecord['path'] = root + "/" + item
        fRecord['lastmodified'] = datetime.fromtimestamp( int( os.path.getmtime(root+"/"+item) ) ).strftime('%Y-%m-%d %H:%M:%S')
        fRecord['filesize'] = fileSize
        _files.append(fRecord)



    fileText = _THEME.replace("$content$", fileText) # Insert the generated page-content into the theme.

    # Theme Variable Insertion here
    fileText = fileText.replace("$root-dir$", root.strip("./"))
    fileText = fileText.replace("$domain$", _DOMAIN)

    # => Handle the Breadcrumbs
    path = root.split("/")
    breadCrumb = ""
    crumbSep = '<a class="smaller" href="#"> > </a>'
    crumbItem = '<a class="smaller" href="$addr$">$name$</a>'
    for crumb in path:
        # First do crumbname
        if crumb == ".":
            breadCrumb += crumbItem.replace("$name$", "")
        else:
            breadCrumb += crumbItem.replace("$name$", crumb.strip("./"))

        # Then crumb's link address
        if path == ["."]:
            crumbAddr = '#'
        else:
            crumbAddr = ('../' * (len(path)-(path.index(crumb)+1)))
            crumbAddr += './'
        breadCrumb = breadCrumb.replace("$addr$", crumbAddr)

        # If is not last item in list, append >
        if crumb != path[-1]:
            breadCrumb += crumbSep

    fileText = fileText.replace("$breadcrumb$", breadCrumb) # write composed breadcrumb to file.

    # Set sidenav dir tree
    fileText = fileText.replace("$sidenav$", _DIRTREE)


    # Set dynamic folder refs.
    fileText = fileText.replace("$root-step$", rootStep)


    # Write the composed HTML to a file.
    try:
        dirFile.write("")
        dirFile.write(fileText)

    except Exception as e:
        console.warn("There was an unhandled error while writing the directory \"" + root + "\"...")
        console.warn("Exception information: " + str(e))
    console.log("Generated entries for " + str(dirCount) + " directories and " + str(fileCount) + " files in folder /" + root.strip("./") + ". Took " + str(round(((clock() - __DIRSTARTTIME__)*1000), 3)) + "ms")
    # print(fileText)

console.log("Loading File Entries into files.json in /includes...")

__DIRSTARTTIME__ = clock()
with open('include/files.json', 'w') as jsonFile:  # Write directory tree information in the include folder as tree.json
    jsonFile.write('var jsonText = \'')
    jsonFile.write(json.dumps(_files).replace('\x00', '').replace(" null,", '').replace(' null', '').replace("null,", '').replace("'", "\\'"))
    jsonFile.write('\'')
console.log("Completed file list JSON generation in " + str(round(((clock() - __DIRSTARTTIME__)*1000), 3)) + "ms")

console.log("Done. Took " + str(round(((clock() - __STARTTIME__)*1000), 3)) + "ms")

# PYDIR

## Generate static HTML pages for directory listings.

This Python Script will scan a given directory and all it contains, recursively, and within each of those directories (including the root) create a directory listing HTML page that not only looks nice but is completely static, removing the need for often bandwidth-intensive client-side handlers. Not only that, but it also has support for custom styles, so no more of those ugly default Apache directory listings.

It first will compile HTML for the folders, then takes file names and calculates file sizes for their listings. It lists in alphabetical order by default.

# Requirements
 - Unix `du` utility. It should be already installed in your Unix or Linux Distro. (Note: Read "Performance" below.)
 - Python 3.5.2 or other compatible version.
 - xxHash: [pip install xxhash](https://cyan4973.github.io/xxHash/)

# Usage

`python3 app.py /path/to/root/working/directory`(Note no ending forward slash!) You may use `.` or any relative naming to describe the directory. Please note that the program will write files to the chosen directory. Also note that the `include` folder will be copied in its entirety to the root directory of the target.

# Configuration

Edit cfg.py to modify user options.

Here are some settings for you to modify.
EXCLUDES => Add in here the file/directory names you do NOT want to be indexed by the program.
ROOTDIR => If you don't want to specify the working directory as a command line argument, uncomment it from the config.
DIRFILENAME => Change the default name of the file from "index.html"
DOMAIN => Set this to the domain name for your site.
ALPHAORDER => Set to true if you want files/folders to be sorted alphabetically in the listings.

FOLLOWSYMLINKS => Set to true to have the program follow symbolic links.
ALLOW_OUT_OF_WEBROOT => Set to false to restrict symlink destinations to only within the `WEBROOT`
WEBROOT => Where to restrict symlinks to. Used in conjunction with `ALLOW_OUT_OF_WEBROOT`


LOGLEVEL => What kinds of messages do you want logged. Levels are -1 for none, 0 for info, 1 for warning, 2 for errors, 3 for verbose.


## These settings are for wizards only (or for those who are willing to read through the code)
ITEMTEMPLATE = open("<filename>").read()  => Set <filename> to the path of whatever file you want to use as the template for individual items in the listing.
THEME = open("<filename>").read() => This is the template html for each page.


SKIPDIRS => Should directories with no changes made since last run be skipped? Turn this off if pages aren't all updating properly.


# Performance
No significant benchmarking has been done, but it handles both many files in a single directory and many files scattered across many directories equally well.
A ~65GB ebooks folder with ~10k loose files scanned completely in 10797.786ms, and a 129GB folder with ~15k files organized meticulously by category finished scanning in 13132.954ms. Suffice to say it makes pretty good time regardless of your needs.
Additionally, it uses the unix utility `du` to scan for file size. Therefore it never has to actually open the file and determine it's size, allowing for files of any size to be scanned. If `du` is not available for any reason, it will default to the universal, albeit slow, python method of opening files. It is reccomended to have `du` installed on your system.

# Search
Search is reasonably fast, and since it uses [lunr.js](https://lunrjs.com) it supports wildcards (`*`) and boosts (`^x`), which allow you to prioritize certain parts of the search by `x` times.

# Examples
See an example page listing (may not always be up to date) at [static.dnd.guide](https://static.dnd.guide)

# Theme-Making
PyDir-gen uses tags to search and insert certain values. Knowing these tags and inserting them into your theme and itemtemplate HTML files is necessary for the tool to work.

First is the `$content$` tag. This goes in your main `theme.html` file and will be replaced with a single instance of `item-template.html` for every file or folder in the current directory.
Inside the `item-template.html` file, there are more tags. The `$class$` tag will be replaced with `icon dir` or `icon file` (referring to css classes) for directories and files, respectively.
The `$file-href$` tag will be replaced with the relative path to the file that that specific entry points to.
`$item-type$ ` will be replaced with `icon dir-icon` or `icon file-icon`, which sets the icons to the left of the entries.
`$root-step$` will be replaced with an amount of `../`'s required to get to the root site directory you specified as a comand line argument (NOT \_WEBROOT).
`$domain$` will be replaced with the domain specified in the config. `$root-dir$` refers to the name of the folder that the final html file will be placed in.
`$sidenav$` will be replaced with an unordered, dropdown list representing a directory tree of the website.
`$breadcrumb$` will be replaced with a hyperlinked breadcrumb leading back to the root working directory.

# FAQ
- Q: Help! Symlinks aren't showing up!
  - A: First, make sure the `FOLLOWSYMLINKS` option is set to true in the config file. If that doesn't work, then make sure you have set the proper webroot in `cfg.py` and there is no trailing slash `/` at the end of it. If you want the symlinks to go out of your set webroot, make sure the appropriate setting is also changed in the config.

- Q: Can I use this for my commercial product/website without crediting you?
  - A: Absolutely! There are a few requirements, though. First, this software must retain the MIT license. Second, I am not liable for what this program does or what you do with it. Use it at your own risk.

- Q: Why is this FAQ so short?
  - A: People don't ask many questions.
# License and Attribution
This work is licensed under the MIT license. Some parts of this work may be licensed differently.
Additionally, there is an attribution in the footer of the default template. Feel free to edit or remove it, but it would be appreciated if it were left in.

# PYDIR
### Generate static HTML pages for directory listings.
This Python Script will scan a given directory and all it contains, recursively, and within each of those directories (including the root) create a directory listing HTML page that not only looks nice but is completely static, removing the need for often bandwidth-intensive client-side handlers. Not only that, but it also has support for custom styles, so no more of those ugly default Apache directory listings.

# Usage
`python3 app.py /path/to/root/working/directory/`
You may use `.` or any relative naming to describe the directory.
Please note that the program will write files to the chosen directory.

# Configuration
Edit cfg.py to modify user options.

# License and Attribution

Additionally, there is an attribution in the footer of the default template. Feel free to edit or remove it, but it would be appreciated if it were left in.

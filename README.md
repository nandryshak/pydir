# PYDIR

## Generate static HTML pages for directory listings.

This Python Script will scan a given directory and all it contains, recursively, and within each of those directories (including the root) create a directory listing HTML page that not only looks nice but is completely static, removing the need for often bandwidth-intensive client-side handlers. Not only that, but it also has support for custom styles, so no more of those ugly default Apache directory listings.

It first will compile HTML for the folders, then takes file names and calculates file sizes for their listings. It lists in alphabetical order by default.

# Requirements
 - Unix `du` utility. It should be already installed in your Unix or Linux Distro. (Note: Read "Performance" below.)
 - Python 3.5.2 or other compatible version.

# Usage

`python3 app.py /path/to/root/working/directory/` You may use `.` or any relative naming to describe the directory. Please note that the program will write files to the chosen directory. Also note that the `include` folder will be copied in its entirety to the root directory of the target. (Currently only implemented for Linux)

# Configuration

Edit cfg.py to modify user options.

# Performance
No significant benchmarking has been done, but it handles both many files in a single directory and many files scattered across many directories equally well.
A ~65GB ebooks folder with ~10k loose files scanned completely in 10797.786ms, and a 129GB folder with ~15k files organized meticulously by category finished scanning in 13132.954ms. Suffice to say it makes pretty good time regardless of your needs.
Additionally, it uses the unix utility `du` to scan for file size. Therefore it never has to actually open the file and determine it's size, allowing for files of any size to be scanned. If `du` is not available for any reason, it will default to the universal, albeit slow, python method of opening files. It is reccomended to have `du` installed on your system.

# Examples
See an example page listing (may not always be up to date) at [static.dnd.guide](https://static.dnd.guide)
# License and Attribution

Additionally, there is an attribution in the footer of the default template. Feel free to edit or remove it, but it would be appreciated if it were left in.

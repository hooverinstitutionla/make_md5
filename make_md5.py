#!/usr/bin/env python
#
# make_md5.py
# Author: Jim Sam
# This script generates an indexed md5 checksum for every file in the directory.
# It does not verify checksums.
#
# To use this:
# 1. add this file to the home directory. (House icon in Finder)
# 2. Open Terminal (Applications > Utilities > Terminal)
# 3. navigate to the folder you want to process
# 4. type "python ~/make_md5.py"
# 5. hit enter.
#

import os
import hashlib

# This function, md5_for_file was copied from StackOverflow. Please see:
# http://stackoverflow.com/questions/1131220/get-md5-hash-of-big-files-in-python#1131238
def md5_for_file(f, block_size=2**20):
    m = hashlib.md5()
    with open(f, "rb" ) as f:
        while True:
            buf = f.read(block_size)
            if not buf:
                break
            m.update( buf )
    return m.hexdigest()

def cycle_files(this_dir):
    for i in this_dir:
        new = i+'.md5'
        if os.path.isfile(new):
            continue
        elif '.md5.' in new:
            continue
        else:
            print "Making MD5 for %s now." % i
            m = md5_for_file(i)
            j = open(new, 'w')
            j.write('; Generated by make_md5.py\r\n')
            j.write(m+' *'+i)
            j.close()

def get_sub_folders(dir1):
    this_dir = []
    sub_folders = []
    for f in dir1:
        if os.path.isdir('./'+f):
            sub_folders = sub_folders + [f]
        else:
            this_dir = this_dir + [f]
    return this_dir, sub_folders

def main():
    this_dir = os.listdir('.')
    file_list, sub_folders = get_sub_folders(this_dir)
    cycle_files(file_list)
    print "\nDone!\n"


if __name__ == '__main__':
    main()

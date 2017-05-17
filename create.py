'''create.py creates md5 checksums for all files in a folder.

This script generates an indexed md5 checksum for every file in the directory.
It does not verify checksums. Please see verify_md5.py for verification. Please
see create_tree.py and verify_tree.py for recursive creation and verification.
'''

import hashlib
import os
import sys

py_version = sys.version_info.major

def md5_for_file(f, block_size=2**20):
    '''This function, md5_for_file was copied from StackOverflow, used under the
    Creative Commons license outlined at:
    http://blog.stackoverflow.com/2009/06/attribution-required/

    StackOverflow User Yuval Adam.
    http://stackoverflow.com/users/24545/yuval-adam
    Code:
    http://stackoverflow.com/questions/1131220/get-md5-hash-of-big-files-in-python#1131238
    '''
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
        if i == '.DS_Store':
            continue
        new = i+'.md5'
        if os.path.isfile(new):
            continue
        elif '.md5.' in new:
            continue
        else:
            try:
                print("Making MD5 for %s now." % i)
            except UnicodeEncodeError:
                print("Making MD5 for a file with special characters in its name now.")
                print("\n* * * * * * * * * * * * * * * * * * * * * * * *\n")
                print("  DOES THIS FILE WITH SPECIAL CHARACTERS IN\n")
                print("  ITS NAME NEED TO BE RENAMED?")
                print("  %s\n" % i.encode())
                print("* * * * * * * * * * * * * * * * * * * * * * * *\n")
            try:
                m = md5_for_file(i)
            except IOError:
                print("\n* * * * * * * * * * * * * * * * * * * * * * * *\n")
                print("An MD5 checksum cannot be generated for %s with this version of Python." % i.encode())
                print("\n* * * * * * * * * * * * * * * * * * * * * * * *\n")
                continue
            if py_version == 2:
                with open(new, 'w') as n:
                    n.write('; Generated by create.py\r\n')
                    n.write('; You may find a copy at https://github.com/hooverinstitutionla/md5_utilities\r\n')
                    n.write(m+' *'+i)
            else:
                with open(new, 'w', encoding='utf8') as n:
                    n.write('; Generated by create.py\r\n')
                    n.write('; You may find a copy at https://github.com/hooverinstitutionla/md5_utilities\r\n')
                    n.write(m+' *'+i)

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
    print("\nDone!\n")


if __name__ == '__main__':
    main()

'''verify.py verifies md5 checksums for all files in a folder.

This script verifies an indexed md5 checksum for every checksum in the directory.
It does not generate checksums. Please see create.py for creation.  Please
see create_tree.py and verify_tree.py for recursive creation and verification.
'''

import datetime
import hashlib
import os
import sys

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

def get_hash(m):
    with open(m, 'r') as f:
        for line in f:
            if ' *' in line:
                a = line.split(' *')
                hashcode = a[0].rstrip().lower()
    return hashcode

def cycle_files(md5_list):
    did_verified = []
    not_verified = []
    missing = []
    for m in md5_list:
        print("Working on %s now." % m)
        verified = False
        filename = m[:-4]
        if filename == '.DS_Store':
            continue
        try:
            generated_hashcode = md5_for_file(filename)
            derived_hashcode = get_hash(m)
            if generated_hashcode == derived_hashcode:
                verified = True
                did_verified.append(filename)
            if not verified:
                not_verified.append(filename)
        except:
            missing.append(filename)

    return did_verified, not_verified, missing

def make_file_list(dir1, ext):
    file_list = []
    for f in dir1:
        file_name=str(f)
        if file_name[-4:].lower() == ext:
            file_list.append(file_name)
    return file_list

def main():
    this_dir = os.listdir('.')
    md5_list = make_file_list(this_dir, '.md5')
    if len(md5_list) == 0:
        print("\n* * * * * * * * * * * * * * * * * * * * * * * *\n")
        print("  The folder does not have any checksums in it.\n")
        print("* * * * * * * * * * * * * * * * * * * * * * * *\n")
        sys.exit()

    print("Compiling files to verify now.\n")
    verified, not_verified, missing = cycle_files(md5_list)

    with open('%s_verification_results.txt' % datetime.date.today(), 'w') as results:
        if len(verified) > 0:
            print("The following verified: \n")
            results.write("The following verified: \n")
            for f in verified:
                print(f)
                results.write(f+"\n")
            results.write("\n")
        else:
            print("\n* * * * * * * * * * * *\n")
            print("  NO FILES VERIFIED!!!\n")
            print("* * * * * * * * * * * *\n")
            results.write("\n* * * * * * * * * * * *\n")
            results.write("  NO FILES VERIFIED!!!\n")
            results.write("* * * * * * * * * * * *\n")

        if len(not_verified) > 0 or len(missing) > 0:
            if len(not_verified) > 0:
                print("\nThe following failed to verify: \n")
                results.write("\nThe following failed to verify: \n")
                for f in not_verified:
                    print(f)
                    results.write(f+'\n')
                results.write("\n")
            if len(missing) > 0:
                print("\nThe following files are missing: \n")
                results.write("\nThe following files are missing: \n")
                for f in missing:
                    print(f)
                    results.write(f+'\n')
                results.write("\n")
        else:
            print("\nHooray! All MD5 files verified!\n")
            results.write("\nHooray! All MD5 files verified!\n\n")

if __name__ == '__main__':
    main()

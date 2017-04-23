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

md5 = sys.argv[1]
f = md5[0:-4]
if md5[-4:] != '.md5':
    sys.exit('That\'s not an MD5 file')
if not os.path.exists(md5):
    sys.exit('That MD5 file does not exist.')
if not os.path.exists(f):
    sys.exit('The file for that MD5 file does not exist')

hash_for_f = get_hash(md5)
temp_hash = md5_for_file(f)

if hash_for_f == temp_hash:
    print('Hooray, %s validates!' % f)
else:
    print('%s does not validate.' % f)

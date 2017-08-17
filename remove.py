import os

for root, dirs, files in os.walk('.'):
    for f in files:
        if f[-4:] == '.md5':
            full = os.path.join(root, f)
            os.remove(full)

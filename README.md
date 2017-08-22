# About

create.py, create_tree.py, verify.py, verify_tree.py, and verify_single.py are complimentary scripts that help ensure fixity for the Hoover Institution Library and Archives.

The purpose of these scripts is to generate and verify an *indexed* sidecar MD5 checksum/hash file for each file in a targeted folder. If .md5 files already exist for a given file, neither create.py nor create_tree.py will not overwrite them.

create.py and verify.py, respectively, create and verify checksums in a single folder.

create_tree.py and verify_tree.py, respectively as above, process a folder and all its subfolders.

verify_single.py validates a single md5 file.

# How to Use

1. Download the scripts (see the big green button above, to the right). Save them somewhere convenient. For sake of example later, we'll say "c:\\scripts".

1. Open your terminal or command prompt. [Windows](https://www.youtube.com/watch?v=VyiGZW0fTxk) [Mac](https://www.youtube.com/watch?v=zw7Nd67_aFw)

2. Navigate to the folder (or top-level folder) you want to process. [Windows](https://www.youtube.com/watch?v=bmGy8Q9eZV8) [Mac](https://www.youtube.com/watch?v=mgazHxDtiu8) (substitute folder for file)

3. Call the script with full path to the script: `python c:\scripts\create.py`. For verify_single, this will look like `python c:\scripts\verify_single.py c:\path\to\fake_file.txt.md5` will verify fake_file.txt.

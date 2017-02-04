create.py and verify.py are complimentary scripts that help ensure fixity for the Hoover Institution Library and Archives.

The purpose of these scripts is to generate and verify an *indexed* sidecar MD5 checksum/hash file for each file in a targeted folder. If .md5 files already exist for a given file, create.py does not overwrite them. They do not recursively walk down subfolders.

create_tree.py and verify_tree.py are complimentary scripts that *do* walk down a folder structure.

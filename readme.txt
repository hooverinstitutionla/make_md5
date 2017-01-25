make_md5.py and verify_md5.py are complimentary programs that help ensure fixity for the Hoover Institution Library and Archives.

The purpose of these programs is to generate and verify an *indexed* sidecar MD5 checksum/hash file for each file in a targeted folder. These programs do not walk through subfolders at this time. If .md5 files already exist for a given file, make_md5.py does not overwrite them.

They were originally written in Python 2.7 to enable ease of use on Macintosh computers. Python 3 compatible versions were then created, noted by the _3 suffix.

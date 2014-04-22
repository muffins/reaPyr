# Nick Anderson 02/24/2014
#
# Digital Forensics, Spring 2014 - CS 6963 Final Project
#
# This program takes as input a Windows disk image, currently only dd
# is supported, and outputs an enumerated list of credentials stored
# on the image. 
#
# Each class of credential type is called a 'Reaper', and
# is designed to target and harvest the specified credential
# type specified in '<name>_rpr.py'
# 
#
#
# TODO:
#
#  1.) Automate the disk mount process
#  2.) Harvest Windows/IE Credentials from windows reg
#    a.) extract registry from tsk recovered files
#  3.) Harvest FF/Chrome Credentials from Win FS
#    a.) Locate where these DB's are
#    b.) Read up on cracking whatever manner of protection exists
#        on these dbs.
#  4.) Add a logging function?
#  5.) Hash out the reaper classes.
#
#
#  Mount the FS with pytsk3. For the schardt disk image, this
#  can be done with the following:
#
## Step 1: get an IMG_INFO object
#img = pytsk3.Img_Info(url)
#
## Step 2: Open the filesystem
#fs = pytsk3.FS_Info(img)
#
## Step 3: Open the directory node this will open the node based on path
## or inode as specified.
#directory = fs.open_dir(path=path, inode=inode)
#
## Step 4: Iterate over all files in the directory and print their
## name. What you get in each iteration is a proxy object for the
## TSK_FS_FILE struct - you can further dereference this struct into a 
## TSK_FS_NAME and TSK_FS_META structs.
#for f in directory:
#        print f.info.meta.size, f.info.name.name
#
#
#
#

import sys
import os
import subprocess
import pytsk3
import argparse

# Main handler. This should fire up classes of all reapers.
def main(di):
    fs  = []
    off = 0
    img = pytsk3.Img_Info(di)
    vol = pytsk3.Volume_Info(img)
    # TODO:
    # Automagically find the NTFS partion(s)
    # and mount each one.
    for ntfs_part in vol:
        fs.append = pytsk3.FS_Info(part, offset=off) 
    # To access the files
    fs[0].open_dir(path=path)#, inode=inodei)
    # see above for more information

if __name__ == "__main__":
    if sys.platform[:3] != 'lin':
        print("reaPyng.py currently only supports linux.")
        sys.exit()
    elif len(sys.argv) != 2:
        print("Usage: %s <Disk Image>" % sys.argv[0])
        sys.exit()
    else:
        # Parse the specified filename to ensure that it exists.
        if os.path.isfile(sys.argv[1]):
            main(sys.argv[1])
        else:
            print("Unable to open %s" % sys.argv[1])
            sys.exit()

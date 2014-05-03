
"""
Nick Anderson 02/24/2014

Digital Forensics, Spring 2014 - CS 6963 Final Project

reaPyr.py

Usage:

    user@system:~$ reaPyr.py [-h] -f FILENAME -d DISKNAME [-o OFFSET] [-ss SECTSIZE]

    File carving from disk images.

    optional arguments:
      -h, --help            show this help message and exit
      -f FILENAME, --filename FILENAME
                            File name to be carved out of the disk image.
      -d DISKNAME, --diskname DISKNAME
                            Name of the disk image to reap.
      -o OFFSET, --offset OFFSET
                            Offset into disk where OS resides. Default is 0.
      -ss SECTSIZE, --sectsize SECTSIZE
                            Sector size of OS. Default is 512 bytes.



See README.md for additional information.


"""

import sys
import os
import subprocess
import pytsk3
import argparse
import disk
import errno

# import the reapers
from windows import win_rpr
from google import google_rpr
from mozilla import mozilla_rpr
from im import im_rpr

# Function to ensure that recovery directory exists.
def create_dir(d):
    try:
        os.makedirs(d)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print "ERROR: Unable to create ./recovered/ and dir does not exists!"
            sys.exit(0)


# What information do I need for this??
"""
    Report Format:
    Reaper Name:
        table of items found:
        name of db, md5sum, file size
                ....
    Reaper Name:
        table of items found:
        name of db, md5sum, file size
                ....
"""
def report():
    pass


# Main handler. This should fire up classes of all reapers.
def reap(img, offs=0, ss=0):
    
    # Create the disk object
    d = disk.Disk(img, offs, ss)

    # Create a directory to stash our harvest!
    create_dir("./harvest")

    # Reap the disk
    win_rpr.reap(d)
    #google_rpr.reap(d)
    #mozilla_rpr.reap(d)
    im_rpr.reap(d)




if __name__ == "__main__":

    if sys.platform[:3] != 'lin':
        print("ERROR: reaPyr currently only runs on linux.")
        sys.exit()

    p = argparse.ArgumentParser(description="This program carves, or reaps, user credentials\
        from a specified disk image.")
    p.add_argument("-d","--diskname",help="Name of the disk image to reap.", required=True)
    p.add_argument("-o","--offset",help="Offset into disk where OS resides.  Default is 0.", required=False)
    p.add_argument("-ss","--sectsize",help="Sector size of OS.  Default is 512 bytes.", required=False)
    args = p.parse_args()

    ss   = 0
    offs = 0

    if args.offset != None:
        offs = int(args.offset)

    if args.sectsize != None:
        ss = int(args.sectsize)

    reap(args.diskname, offs, ss)



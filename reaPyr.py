
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


TODO:

* IE, Thunderbird, Outlook

* Fix Firefox Carving

* Add/Check Vista+ Support




"""

import sys
import os
import subprocess
import pytsk3
import argparse
import disk
import errno
import hashlib

# import the reapers
from windows import win_rpr
from google import google_rpr
from mozilla import mozilla_rpr
from im import im_rpr

# Define here the Disk Recovery Directory.  This will need to be
# changed in ALL reaper files if altered :(  AS well as in disk.py
rec_dir     = "./disk_rec"
harvest_dir = "./harvest"
report_name = "./report.csv"

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
# This function reports any findings from the specified reaper.
# TODO: Decide on format for the report.  Is CSV better? or should I
# consider doing something like XML or try to finagle a PDF??
def report(harvest):
    global report_name
    fout = open(report_name, 'a')
    for s in harvest:
        fout.write(s+"\n")
    fout.close()


# This function moves all of the harvested files from './disk_rec/' to 
# their respective harvest folder. ./harvest/'rpr_name'/
# Argument specified is the target folder in ./harvest
def clean(rpr_name):
    global rec_dir, harvest_dir
    for f in os.listdir(rec_dir):
        os.rename(os.path.join(rec_dir, f), os.path.join(harvest_dir,rpr_name,f))


# Main handler. This should fire up classes of all reapers.
def reap(img, offs=0, ss=0):
    global harvest_dir
    # Create the disk object
    d = disk.Disk(img, offs, ss)

    # Create a directory to stash our harvest!
    create_dir(harvest_dir)
    create_dir(os.path.join(harvest_dir,"windows"))
    create_dir(os.path.join(harvest_dir,"google"))
    create_dir(os.path.join(harvest_dir,"mozilla"))
    create_dir(os.path.join(harvest_dir,"im"))

    """
        Reap the Disk

        ** TODO: Think about if the clean/report actions should happen
        inside of the reapers, essentially, who's responsibility is it
        to report the data, and cleanup the disk_rec folder.

        A Reaping happens as a triple of actions.  Firstly the respective
        reaper is called, to harvest any possible data.  Afterwords reaPyr
        itself will report any of findings, and lastly clean the 'disk_rec'
        directory so the next reaper can be run.
    """
    # Write out the title row
    report(["Reaper Name,Carved File Name,SHA1Sum,Size of File,Description"])

    # Reap Windows
    report(win_rpr.reap(d))
    clean("windows")

    # Reap Google
    report(google_rpr.reap(d))
    clean("google")

    # Reap Mozilla
    report(mozilla_rpr.reap(d))
    clean("mozilla")
    
    # Reap IM
    report(im_rpr.reap(d))
    clean("im")




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



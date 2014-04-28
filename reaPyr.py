
"""
 Nick Anderson 02/24/2014

 Digital Forensics, Spring 2014 - CS 6963 Final Project



Notes:

    At this point, reaPyr needs to bring in the following things

    * Disk Image name
    * Offset into the disk image where the OS resides
    * 


Future Work:
    * Make a 'Disk' class out of the functionality in the fs_walk,
    so that reaPyr's only job is to make the Disk object, and then
    hand that off to each reaper.

    * Add multiple OS support.

"""



import sys
import os
import subprocess
import pytsk3
import argparse
import disk

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

    p = argparse.ArgumentParser(description="File carving from disk images.")
    p.add_argument("-f","--filename",help="File name to be carved out of the disk image.", required=True)
    p.add_argument("-d","--diskname",help="Name of the disk image to reap.", required=True)
    p.add_argument("-o","--offset",help="Offset into disk where OS resides.  Default is 0.", required=False)
    p.add_argument("-ss","--sectsize",help="Sector size of OS.  Default is 512 bytes.", required=False)
    args = p.parse_args()



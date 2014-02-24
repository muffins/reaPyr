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
# 1.) Add harvesting for Windows OS
#   a.) Windows Credentials
#   b.) Browser Credentials
#   c.) 3rd Party IMs (IRC, GTalk, Hangouts, etc...)

import sys, os

# Main handler. This should fire up classes of all reapers.
def main(di):
    pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: %s <Disk Image>" % sys.argv[0])
        sys.exit()
    else:
        # Parse the specified filename to ensure that it exists.
        if os.path.isfile(sys.argv[1]):
            main(sys.argv[1])
        else:
            print("Unable to open %s" % sys.argv[1])
            sys.exit()

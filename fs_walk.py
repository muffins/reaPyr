#!/usr/bin/python
import sys
import argparse
import pytsk3
import os
import errno

# Globals Section
CFILE 		= ""
SECT_SIZE 	= 512
PART_OFFS 	= 0
REC_CNT		= 0

# Function to ensure that recovery directory exists.
def create_dir(d):
    try:
        os.makedirs(d)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print "ERROR: Unable to create ./recovered/ and dir does not exists!"
            sys.exit(0)

# Carve files from .dd and write them to ./recovered/
def fs_walk(cwd, fs):
	global CFILE, REC_CNT

	try: directory = fs.open_dir(cwd)
	except IOError as e:
		# Fail silently for now.
		#print "ERROR: Unable to open directory, path not found - %s" % cwd
		return

	# Walk through each item found in the directory opened by tsk
	for f in directory:
		# $OrphanFiles is a container of unallocated files in Windows, TSK Segfaults on
		# attempting to parse these files, so for the moment we cannot recover data located
		# in $OrphanFiles
		if "$OrphanFiles" in f.info.name.name: continue
		elif f.info.name.name != '.' and f.info.name.name != '..':
			# If the file has no type, it's likely been marked 'unallocated'
			# and tsk will return it's type as None.  We simply skip these.
			ftype = pytsk3.TSK_FS_META_TYPE_ENUM
			try: ftype = f.info.meta.type
			except: continue
			fname_abs = os.path.join(cwd,f.info.name.name)
			# Recovered filename.  This is used in the event multiple files with
			# the same name are recovered, we will print a '-' delimited file name
			# containing the absolute path on disk to the recovered file.
			fname_rec = '-'.join(fname_abs.split('/'))[1:]


			# The file is just a regular file
			if ftype == pytsk3.TSK_FS_META_TYPE_REG and f.info.name.name == CFILE:

				# Setup environment for file carving
				fi   = fs.open_meta(f.info.meta.addr)
				#fout = open(os.path.join("./recovered",f.info.name.name), 'wb')
				fout = open(os.path.join("./recovered",fname_rec), 'wb')
				offs = 0
				size = fi.info.meta.size
				BUFF_SIZE = 1024*1024

				# Recunstruct the file from the inodes
				while offs < size:
					atr = min(BUFF_SIZE, size - offs)
					d = fi.read_random(offs, atr) # Why does he do read_rand?
					if not d: break
					offs += len(d)
					fout.write(d)
				fout.close()

				# Indicate the number of files we've recovered
				REC_CNT += 1

			# Recurse down directories.
			elif ftype == pytsk3.TSK_FS_META_TYPE_DIR: fs_walk(fname_abs, fs)
			# If the item wasn't a file/directory, we don't care about it.
			else: pass

# Handler function for fs_walk, this 'sets the stage'
def fs_walk_handler(img="", fname="", offs=0, ss=0):
	global CFILE, SECT_SIZE, PART_OFFS, REC_CNT

	# Stash the desired file name for what we want to carve.
	CFILE 	= fname
	if ss 	!= 0: SECT_SIZE = ss
	if offs != 0: PART_OFFS = offs

	# Use TSK to open the disk image
	if os.path.exists(img):
		# Create the outfile directory
		create_dir("./recovered")

		# Use TSK to open up the disk image
		img   = pytsk3.Img_Info(img)
		fs    = pytsk3.FS_Info(img, offset=PART_OFFS*SECT_SIZE)

		# Recursively walk through the image, looking for our file.
		fs_walk("/",fs)
	else:
		print "Unable to find disk image %s!  Exiting." % img
		sys.exit(0)

	if(REC_CNT):
		print "###################################################################"
		print "## reaPying completed.  Recovered %d files. Any recovered files \n## have been written out to ./recovered/" % REC_CNT
		print "###################################################################"
	else:
		print "###################################################################"
		print "## reaPying completed.  No files named %s recovered" % fname
		print "###################################################################"




if __name__ == "__main__":

	p = argparse.ArgumentParser(description="File carving from disk images.")
	p.add_argument("-f","--filename",help="File name to be carved out of the disk image.", required=True)
	p.add_argument("-d","--diskname",help="Name of the disk image to reap.", required=True)
	p.add_argument("-o","--offset",help="Offset into disk where OS resides.  Default is 0.", required=False)
	p.add_argument("-ss","--sectsize",help="Sector size of OS.  Default is 512 bytes.", required=False)
	args = p.parse_args()

	if args.offset != None and args.sectsize != None:
		fs_walk_handler(args.diskname, args.filename, int(args.offset), int(args.sectsize))
	elif args.offset != None:
		fs_walk_handler(args.diskname, args.filename, int(args.offset))
	elif args.sectsize != None:
		fs_walk_handler(args.diskname, args.filename, 0, int(args.sectsize))
	else:
		fs_walk_handler(args.diskname, args.filename)

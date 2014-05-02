#!/usr/bin/python


"""
Nick Anderson

fs_walk.py

File System Walker - This program uses The Sleuth Kit bindings
to carve a Windows disk image in search of a specified file.  The
program then 'carves' this file out of the disk image and stores
it in a folder named 'recovered'

"""

import sys
import argparse
import pytsk3
import os
import errno


class Disk:
	# Globals Section
	fs        = pytsk3.Object
	seekf     = ""
	abseekf   = ""
	sect_size = 512
	part_offs = 0
	rec_cnt   = 0
	buff_size = 1024*1024


	# Handler function for fs_walk, this 'sets the stage'
	def __init__(self, img="", offs=0, ss=0):

		# Setup sector and offset if provided.
		if ss 	!= 0: self.sect_size = ss
		if offs != 0: self.part_offs = offs

		# Use TSK to open the disk image
		if os.path.exists(img):
			# Create the outfile directory
			self.create_dir("./disk_rec")

			# Use TSK to open up the disk image
			img     = pytsk3.Img_Info(img)
			self.fs = pytsk3.FS_Info(img, offset=self.part_offs*self.sect_size)

		else:
			print "Unable to find disk image %s!  Exiting." % img
			sys.exit(0)


	# Function to ensure that recovery directory exists.
	def create_dir(self, d):
	    try:
	        os.makedirs(d)
	    except OSError as e:
	        if e.errno != errno.EEXIST:
	            print "ERROR: Unable to create ./recovered/ and dir does not exists!"
	            sys.exit(0)

	# Given the absolute file path to a specified file, try to carve the file
	def carve(self, abseekf):
		cwd   = '/'.join(abseekf.split('/')[:-1])
		fname = abseekf.split('/')[-1]

		try: f = self.fs.open(abseekf)
		except IOError as e:
			print "ERROR: Unable to open %s" % abseekf
			sys.exit()
				
		# Make sure that the desired file is actually a file.
		ftype = pytsk3.TSK_FS_META_TYPE_ENUM
		try: ftype = f.info.meta.type
		except:
			print "ERROR: File opened had no meta type!"
			sys.exit()

		if ftype == pytsk3.TSK_FS_META_TYPE_REG:

			# Setup environment for file carving
			fi   = self.fs.open_meta(f.info.meta.addr)
			fout = open(os.path.join("./disk_rec",fname), 'wb')
			offs = 0
			size = fi.info.meta.size

			# Recunstruct the file from the inodes
			while offs < size:
				atr = min(self.buff_size, size - offs)
				d   = fi.read_random(offs, atr) # Why does he do read_rand?
				if not d: break
				offs += len(d)
				fout.write(d)
			fout.close()

			# Indicate the number of files we've recovered
			self.rec_cnt += 1
		else:
			print "ERROR: %s is not a file!"
			sys.exit()

	# Return a directory listing of 'd', similar to ls or dir.
	def dir_carve(self, d):

		try: directory = self.fs.open(d)
		except IOError as e:
			print "ERROR: Unable to open %s" % d
			sys.exit()
				
		# Make sure that the desired file is actually a file.
		ftype = pytsk3.TSK_FS_META_TYPE_ENUM
		try: ftype = f.info.meta.type
		except:
			print "ERROR: File opened had no meta type!"
			sys.exit()

		dir_list = []
		if ftype == pytsk3.TSK_FS_META_TYPE_DIR:
			for f in directory:
				if f.info.name.name != '.' and f.info.name.name != '..':
					dir_list.append(f)
		else:
			print "ERROR: %s is not a directory!"
			sys.exit()

	# Walk the disk, looking for the desired file to carve.
	def search_carve(self, cwd, seekf):
		try: directory = self.fs.open_dir(cwd)
		except IOError as e:
			# If we are not able to open the directory, tank out
			# and continue execution.  This should be changed in the future
			# to allow for more robust searching of the disk drive.
			#print "ERROR: Unable to open %s" % cwd
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
				if ftype == pytsk3.TSK_FS_META_TYPE_REG and f.info.name.name == seekf:

					# Setup environment for file carving
					fi   = self.fs.open_meta(f.info.meta.addr)
					fout = open(os.path.join("./disk_rec",fname_rec), 'wb')
					offs = 0
					size = fi.info.meta.size
					

					# Recunstruct the file from the inodes
					while offs < size:
						atr = min(self.buff_size, size - offs)
						d = fi.read_random(offs, atr) # Why does he do read_rand?
						if not d: break
						offs += len(d)
						fout.write(d)
					fout.close()

					# Indicate the number of files we've recovered
					self.rec_cnt += 1

				# Recurse down directories.
				elif ftype == pytsk3.TSK_FS_META_TYPE_DIR: self.search_carve(fname_abs, seekf)
				# If the item wasn't a file/directory, we don't care about it.
				else: pass






# Main entry point
if __name__ == "__main__":

	p = argparse.ArgumentParser(description="File carving from disk images.")
	p.add_argument("-f","--filename",help="File name to be carved out of the disk image.", required=True)
	p.add_argument("-d","--diskname",help="Name of the disk image to reap.", required=True)
	p.add_argument("-o","--offset",help="Offset into disk where OS resides.  Default is 0.", required=False)
	p.add_argument("-ss","--sectsize",help="Sector size of OS.  Default is 512 bytes.", required=False)
	p.add_argument("-a","--absolute",action='store_true',help="Filename provided is an absolute path to the desired file. [T|F]", required=False)
	args = p.parse_args()

	offs = 0
	ss   = 0

	if args.offset != None:
		offs = int(args.offset)

	if args.sectsize != None:
		ss = int(args.sectsize)
	
	d = Disk(args.diskname, offs, ss)

	if args.absolute: 
		d.carve(args.filename)
	else: 
		d.search_carve("/", args.filename)

"""

	Windows Reaper

	This script makes use of the disk handed to us by reaPyr and
	attempts to carve out the Windows NT password hashes, as well
	as any cached/saved passwords from IE

	Food for thought:

	* Delete the disk_rec contents when completed

	* copy the win_hrvst.txt file somewhere to the root
	directory when completed.

	* Change the way that recovered file renaming is handled

"""
import sys, os, hashlib

sys.path.append("./windows/creddump")

from framework.win32.domcachedump import dump_file_hashes as cachedump
from framework.win32.hashdump import dump_file_hashes as pwdump
from framework.win32.lsasecrets import get_file_secrets as lsadump


# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/142812
FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])

def dump(src, length=8):
	N=0; result=''
	while src:
		s,src = src[:length],src[length:]
		hexa = ' '.join(["%02X"%ord(x) for x in s])
		s = s.translate(FILTER)
		result += "%04X   %-*s   %s\n" % (N, length*3, hexa, s)
		N+=length
	return result

"""
	Main function for any reaper.  Should return a list of CSV strings,
	each one detailing any files harvested.
"""
def reap(d):
	# Registry hives containing NTLM password hashes.
	
	harvest  = [] # Return value
	rpr_name = "im"

	"""
		Pidgin Harvesting
	"""

	desc     = "Pidgin cached credentials file"
	appdata_xp = "/Documents and Settings"
	appdata_vi = "/Users"

	users_xp = d.dir_carve(appdata_xp)
	users_vi = d.dir_carve(appdata_vi)

	# Reap XP
	if users_xp	!= [] and "ERROR" not in users_xp:
		for u in users_xp:
			fname = d.carve(appdata_xp+'/'+u+'/Application Data/.purple/accounts.xml')
			if os.path.exists(fname):
				# Rename the file to include the user name, in case we have multiple users
				f = u+"_xp_"+fname.split('/')[-1]
				dest_fname = os.path.join(d.rec_dir,f)
				os.rename(fname,dest_fname)

				# Append the harvested file information to the list
				sha1   = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
				fsize  = os.path.getsize(dest_fname)
				harvest.append(rpr_name+","+f+","+sha1+","+str(fsize)+","+desc)


	# Reap Vista+
	elif users_vi != [] and "ERROR" not in users_vi:
		for u in users_vi:
			fname = d.carve(appdata_vi+'/'+u+'/Application Data/.purple/accounts.xml')
			if os.path.exists(fname):
				# Rename the file to include the user name, in case we have multiple users
				f = u+"_vi_"+fname.split('/')[-1]
				os.rename(fname,os.path.join(d.rec_dir,f))

				# Append the harvested file information to the list
				sha1   = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
				fsize  = os.path.getsize(dest_fname)
				harvest.append(rpr_name+","+f+","+sha1+","+str(fsize)+","+desc)

	"""
		Skype Harvesting
	"""

	

	return harvest
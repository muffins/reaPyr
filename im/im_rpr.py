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
	
	"""
		Carve Pidgin .purple accounts file
	"""

	#C:\Documents and Settings\Administrator\Application Data\.purple  # Pidgin Accounts file

	appdata_xp = "/Documents and Settings"
	appdata_vi = "/Users"

	users_xp = d.dir_carve(appdata_xp)
	users_vi = d.dir_carve(appdata_vi)

	if users_xp	!= [] and "ERROR" not in users_xp:
		for u in users_xp:
			print u
	elif users_vi != [] and "ERROR" not in users_vi:
		for u in users_vi:
			print u

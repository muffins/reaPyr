"""

	Windows Reaper

	This script makes use of the disk handed to us by reaPyr and
	attempts to carve out the Windows NT password hashes, as well
	as any cached/saved passwords from IE

"""



def reap(d):
	# Registry hives containing NTLM password hashes.
	fout = open("./win_hrvst.txt",'a')

	sam_db = "/Windows/system32/config/SAM"
	sys_db = "/Windows/system32/config/system"
	sec_db = "/Windows/system32/config/security"

	d.carve(sam_db)
	d.carve(sys_db)
	d.carve(sec_db)

	# Now, pass off the registry files we just obtained to creddump-0.3
	#
	# https://code.google.com/p/creddump/
	#
	# Thanks Internet!





















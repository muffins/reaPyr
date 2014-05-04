"""

	Google Reaper

	This script makes use of the disk handed to us by reaPyr and
	attempts to carve out any Google passwords on disk.  Currently
	does nothing more than carve out the key3.db file and write it
	out to the disk_rec folder.

"""
import sys, os, hashlib

def reap(d):
	
	harvest  = []

	"""
		Chrome Harvesting
	"""
	rpr_name = "google"
	desc     = "Google Chrome cached credentials file"

	ad_xp_1 = "/Documents and Settings"
	ad_xp_2 = "/Local Settings/Application Data/Google/Chrome/User Data/Default/Web Data"

	ad_vi_1 = "/Users"
	ad_vi_2 = "/Appdata/Local/Google/Chrome/User Data/Default/Web Data"

	users_xp = d.dir_carve(ad_xp_1)
	users_vi = d.dir_carve(ad_vi_1)

	if users_xp	!= [] and "ERROR" not in users_xp:
		for u in users_xp:
			fname = d.carve(ad_xp_1+"/"+u+ad_xp_2)
			if os.path.exists(fname):
				f = u+"_xp_"+fname.split('/')[-1]
				os.rename(fname,os.path.join(d.rec_dir,f))

				# Append the harvested file information to the list
				dest_fname = os.path.join(d.rec_dir,f)
				sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
				fsize      = os.path.getsize(dest_fname)
				harvest.append(rpr_name+","+f+","+sha1+","+str(fsize)+","+desc)

	elif users_vi != [] and "ERROR" not in users_vi:
		for u in users_vi:
			fname = d.carve(ad_vi_1+"/"+u+ad_vi_2)
			if os.path.exists(fname):
				f = u+"_vi_"+fname.split('/')[-1]
				os.rename(fname,os.path.join(d.rec_dir,f))

				# Append the harvested file information to the list
				dest_fname = os.path.join(d.rec_dir,f)
				sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
				fsize      = os.path.getsize(dest_fname)
				harvest.append(rpr_name+","+f+","+sha1+","+str(fsize)+","+desc)

	return harvest


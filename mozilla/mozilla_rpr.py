"""

	Mozilla Reaper

	This script makes use of the disk handed to us by reaPyr and
	attempts to carve out any Mozilla passwords on disk.  Currently
	does nothing more than carve out the key3.db file and write it
	out to the disk_rec folder.

"""
import sys, os, hashlib

def reap(d):
	
	harvest  = []
	rpr_name = "mozilla"
	
	key3db_n    = "key3.db"
	sgnondb1_n  = "signons.sqlite"
	sgnondb2_n  = "signons2.sqlite"
	sgnondb3_n  = "signons3.sqlite"
	sgnontxt1_n = "signons.txt"
	sgnontxt2_n = "signons.txt2"
	sgnontxt3_n = "signons.txt3"

	ad_xp_1 = "/Documents and Settings"
	ad_xp_2 = "/Application Data/Mozilla/Firefox/Profiles"

	ad_vi_1 = "/Users"
	ad_vi_2 = "/Appdata/Roaming/Mozilla/Firefox/Profiles"


	users_xp = d.dir_carve(ad_xp_1)
	users_vi = d.dir_carve(ad_vi_1)

	"""

	TODO: Make this not fucking disgusting.  There's gotta be a better way.
	For the sake of time, I'm leaving it as such, as it works, and I feel it's
	not HORRIBLY broken.

	"""

	if users_xp	!= [] and "ERROR" not in users_xp:
		for u in users_xp:
			ffdb_tmp = ad_xp_1 + "/" + u + ad_xp_2
			profiles = d.dir_carve(ffdb_tmp)
			for p in profiles:

				key3db = ffdb_tmp + "/" + p + "/" + key3db_n
				fname  = d.carve(key3db)
				if not "ERROR" in fname:
					os.rename(fname,os.path.join(d.rec_dir,p+"_xp_"+key3db_n))
					fname = p+"_xp_"+key3db_n

					# Append the harvested file information to the list
					desc       = "Firefox key3db encrypted credentials DB"
					dest_fname = os.path.join(d.rec_dir,fname)
					sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
					fsize      = os.path.getsize(dest_fname)
					harvest.append(rpr_name+","+fname+","+sha1+","+str(fsize)+","+desc)

				sgnondb1 = ffdb_tmp + "/" + p + "/" + sgnondb1_n
				fname    = d.carve(sgnondb1)
				if not "ERROR" in fname:
					os.rename(fname,os.path.join(d.rec_dir,p+"_xp_"+sgnondb1_n))
					fname    = p+"_xp_"+sgnondb1_n

					# Append the harvested file information to the list
					desc       = "Firefox Signon2 SQLite DB #1"
					dest_fname = os.path.join(d.rec_dir,fname)
					sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
					fsize      = os.path.getsize(dest_fname)
					harvest.append(rpr_name+","+fname+","+sha1+","+str(fsize)+","+desc)

				sgnondb2 = ffdb_tmp + "/" + p + "/" + sgnondb2_n
				fname    = d.carve(sgnondb2)
				if not "ERROR" in fname:
					os.rename(fname,os.path.join(d.rec_dir,p+"_xp_"+sgnondb2_n))
					fname = p+"_xp_"+sgnondb2_n

					# Append the harvested file information to the list
					desc       = "Firefox Signon SQLite DB #2"
					dest_fname = os.path.join(d.rec_dir,fname)
					sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
					fsize      = os.path.getsize(dest_fname)
					harvest.append(rpr_name+","+fname+","+sha1+","+str(fsize)+","+desc)

				sgnondb3 = ffdb_tmp + "/" + p + "/" + sgnondb3_n
				fname    = d.carve(sgnondb3)
				if not "ERROR" in fname:
					os.rename(fname,os.path.join(d.rec_dir,p+"_xp_"+sgnondb3_n))
					fname = p+"_xp_"+sgnondb3_n

					# Append the harvested file information to the list
					desc       = "Firefox Signon SQLite DB #3"
					dest_fname = os.path.join(d.rec_dir,fname)
					sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
					fsize      = os.path.getsize(dest_fname)
					harvest.append(rpr_name+","+fname+","+sha1+","+str(fsize)+","+desc)

				sgnontxt1 = ffdb_tmp + "/" + p + "/" + sgnontxt1_n
				fname     = d.carve(sgnontxt1)
				if not "ERROR" in fname:
					os.rename(fname,os.path.join(d.rec_dir,p+"_xp_"+sgnontxt1_n))
					fname     = p+"_xp_"+sgnontxt1_n

					# Append the harvested file information to the list
					desc       = "Firefox Signon2 SQLite TXT #1 - Legacy! Encrypted with 3DES."
					dest_fname = os.path.join(d.rec_dir,fname)
					sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
					fsize      = os.path.getsize(dest_fname)
					harvest.append(rpr_name+","+fname+","+sha1+","+str(fsize)+","+desc)

				sgnontxt2 = ffdb_tmp + "/" + p + "/" + sgnontxt2_n
				fname     = d.carve(sgnontxt2)
				if not "ERROR" in fname:
					os.rename(fname,os.path.join(d.rec_dir,p+"_xp_"+sgnontxt2_n))
					fname = p+"_xp_"+sgnontxt2_n

					# Append the harvested file information to the list
					desc       = "Firefox Signon2 SQLite TXT #2 - Legacy! Encrypted with 3DES."
					dest_fname = os.path.join(d.rec_dir,fname)
					sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
					fsize      = os.path.getsize(dest_fname)
					harvest.append(rpr_name+","+fname+","+sha1+","+str(fsize)+","+desc)

				sgnontxt3 = ffdb_tmp + "/" + p + "/" + sgnontxt3_n
				fname     = d.carve(sgnontxt3)
				if not "ERROR" in fname:
					os.rename(fname,os.path.join(d.rec_dir,p+"_xp_"+sgnontxt3_n))
					fname = p+"_xp_"+sgnontxt3_n

					# Append the harvested file information to the list
					desc       = "Firefox Signon2 SQLite TXT #3 - Legacy! Encrypted with 3DES."
					dest_fname = os.path.join(d.rec_dir,fname)
					sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
					fsize      = os.path.getsize(dest_fname)
					harvest.append(rpr_name+","+fname+","+sha1+","+str(fsize)+","+desc)


	elif users_vi != [] and "ERROR" not in users_vi:
			ffdb_tmp = ad_vi_1 + "/" + u + ad_vi_2
			profiles = d.dir_carve(ffdb_tmp)
			for p in profiles:

				key3db = ffdb_tmp + "/" + p + "/" + key3db_n
				fname  = d.carve(key3db)
				if not "ERROR" in fname:
					os.rename(fname,os.path.join(d.rec_dir,p+"_vi_"+key3db_n))
					fname  = p + "_vi_" + key3db_n

					# Append the harvested file information to the list
					desc       = "Firefox key3db encrypted credentials DB"
					dest_fname = os.path.join(d.rec_dir,fname)
					sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
					fsize      = os.path.getsize(dest_fname)
					harvest.append(rpr_name+","+fname+","+sha1+","+str(fsize)+","+desc)

				sgnondb1 = ffdb_tmp + "/" + p + "/" + sgnondb1_n
				fname    = d.carve(sgnondb1)
				if not "ERROR" in fname:
					os.rename(fname,os.path.join(d.rec_dir,p+"_vi_"+sgnondb1_n))
					fname  = p+"_vi_"+sgnondb1_n

					# Append the harvested file information to the list
					desc       = "Firefox Signon2 SQLite DB #1"
					dest_fname = os.path.join(d.rec_dir,fname)
					sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
					fsize      = os.path.getsize(dest_fname)
					harvest.append(rpr_name+","+fname+","+sha1+","+str(fsize)+","+desc)

				sgnondb2 = ffdb_tmp + "/" + p + "/" + sgnondb2_n
				fname    = d.carve(sgnondb2)
				if not "ERROR" in fname:
					os.rename(fname,os.path.join(d.rec_dir,p+"_vi_"+sgnondb2_n))
					fname  = p+"_vi_"+sgnondb2_n

					# Append the harvested file information to the list
					desc       = "Firefox Signon SQLite DB #2"
					dest_fname = os.path.join(d.rec_dir,fname)
					sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
					fsize      = os.path.getsize(dest_fname)
					harvest.append(rpr_name+","+fname+","+sha1+","+str(fsize)+","+desc)

				sgnondb3 = ffdb_tmp + "/" + p + "/" + sgnondb3_n
				fname    = d.carve(sgnondb3)
				if not "ERROR" in fname:
					os.rename(fname,os.path.join(d.rec_dir,p+"_vi_"+sgnondb3_n))
					fname  = p+"_vi_"+sgnondb3_n

					# Append the harvested file information to the list
					desc       = "Firefox Signon SQLite DB #3"
					dest_fname = os.path.join(d.rec_dir,fname)
					sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
					fsize      = os.path.getsize(dest_fname)
					harvest.append(rpr_name+","+fname+","+sha1+","+str(fsize)+","+desc)

				sgnontxt1 = ffdb_tmp + "/" + p + "/" + sgnontxt1_n
				fname     = d.carve(sgnontxt1)
				if not "ERROR" in fname:
					os.rename(fname,os.path.join(d.rec_dir,p+"_vi_"+sgnontxt1_n))
					fname  = p+"_vi_"+sgnontxt1_n

					# Append the harvested file information to the list
					desc       = "Firefox Signon2 SQLite TXT #1 - Legacy! Encrypted with 3DES."
					dest_fname = os.path.join(d.rec_dir,fname)
					sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
					fsize      = os.path.getsize(dest_fname)
					harvest.append(rpr_name+","+fname+","+sha1+","+str(fsize)+","+desc)

				sgnontxt2 = ffdb_tmp + "/" + p + "/" + sgnontxt2_n
				fname     = d.carve(sgnontxt2)
				if not "ERROR" in fname:
					os.rename(fname,os.path.join(d.rec_dir,p+"_vi_"+sgnontxt2_n))
					fname  = p+"_vi_"+sgnontxt2_n

					# Append the harvested file information to the list
					desc       = "Firefox Signon2 SQLite TXT #2 - Legacy! Encrypted with 3DES."
					dest_fname = os.path.join(d.rec_dir,fname)
					sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
					fsize      = os.path.getsize(dest_fname)
					harvest.append(rpr_name+","+fname+","+sha1+","+str(fsize)+","+desc)

				sgnontxt3 = ffdb_tmp + "/" + p + "/" + sgnontxt3_n
				fname     = d.carve(sgnontxt3)
				if not "ERROR" in fname:
					os.rename(fname,os.path.join(d.rec_dir,p+"_vi_"+sgnontxt3_n))
					fname  = p+"_vi_"+sgnontxt3_n

					# Append the harvested file information to the list
					desc       = "Firefox Signon2 SQLite TXT #3 - Legacy! Encrypted with 3DES."
					dest_fname = os.path.join(d.rec_dir,fname)
					sha1       = hashlib.sha1(open(dest_fname, 'rb').read()).hexdigest()
					fsize      = os.path.getsize(dest_fname)
					harvest.append(rpr_name+","+fname+","+sha1+","+str(fsize)+","+desc)

	return harvest


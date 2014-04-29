![alt tag](https://github.com/PoppySeedPlehzr/reaPyr/raw/master/imgs/reaper.jpg)
```
                                           ______           
                                           | ___ \          
                             _ __ ___  __ _| |_/ /   _ _ __ 
                            | '__/ _ \/ _` |  __/ | | | '__|
                            | | |  __/ (_| | |  | |_| | |   
                            |_|  \___|\__,_\_|   \__, |_|   
                                                  __/ |     
                                                 |___/  
```

Digital Forensics, Spring 2014 - CS 6963 Final Project

###About
    
reaPyr utilizes the pytsk3 framework to carve off of a specified
disk image the credential hashes for Windows, Mozilla, Chrome, and
various other accounts.  The purpose of this software is to aid in
investigations in which one may not have access to account credentials.

The hope being that as many often use the same account credentials
for multiple accounts, if we can glean one set of credentials we
may be able to unlock other accounts as well using the same credential
sets.


###Usage

```bash
user@system:~$ reaPyr.py [-h] -d DiskImage [-o OS Offset (Default 0)] [-ss Sector Size (Default 512)]

File carving from disk images.

optional arguments:
  -h, --help            show this help message and exit
  -d DISKNAME, --diskname DISKNAME
                        Name of the disk image to reap.
  -o OFFSET, --offset OFFSET
                        Offset into disk where OS resides. Default is 0.
  -ss SECTSIZE, --sectsize SECTSIZE
                        Sector size of OS. Default is 512 bytes.
```

###TODO
* Think about deleting ./disk_rec/ after each reap
* Think about aggregating harvest files to central_harvest in main dir
* Add IE Harvesting Support
* Add FF Harvesting Support
* Add Chrome Harvesting Support
* Add IM Harvesting Support

###Future Work
* Add support for running on multiple OS
* Add reapers for multiple OS

###Author

Nick Anderson - nba237@nyu.edu

###Citations

* Thanks to someone awesome for the baller image of an SC2 Reaper.  Link [here](http://static.giantbomb.com/uploads/original/15/155745/2263839-terran_reaper__starcraft_ii_by_oxoxoxo.jpg)

* [creddump](https://code.google.com/p/creddump/)



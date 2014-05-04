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

reaPyr is designed to carve credential sets from Windows XP, however
the foundation is currently in place to attempt to harvest credentials
from Windows Vista+, however this functionality has not been thoroughly
tested and as such may be quite buggy.

reaPyr utilizes the [pytsk3 framework](https://code.google.com/p/pytsk/wiki/pytsk3) to carve off of a specified
disk image the credential hashes and encrypted credential databases
for Windows, Mozilla, Google, and various other programs that allow
you the option of caching credentials. The purpose of this software is 
to aid in forensic investigations in which one may not have access to
specific account credentials. The hope being that as many users often 
utilize the same account credentials for multiple accounts, if we can 
glean one set of credentials we may be able to unlock other accounts 
as well using the same credential sets.

Currently reaPyr simply carves out encrypted databases and looks for
cleartext credential sets. Any data recovered by reaPyr is designed
to be handed off to other 3rd party applications designed for cracking
or getting around software encryption for stored databases.

The credential sets which reaPyr currently harvests are as follows:
* Windows NTLM Accounts
* Windows Cached Credentials
* Windows LSA Secrets
* Internet Explorer
* Mozilla Firefox
* Google Chrome
* Skype
* Pidgin Accounts

###Harvest

Upon completion, the reaPyr program will write out a 'harvest' directory
in which will exist a folder for each reaper file to write out any
data successfully carved from the disk.  Alongside this 'harvest' folder
will be a file in the root directory, report.csv, containing a report
on all of the data carved from the disk.

###Implementation Notes

* Each reaper should be stored in it's own respective directory, for
example the win_rpr.py file lives in the './windows' directory, where
a __init__.py folder lives.  This allows for reaper isolation.

* Each reaper should write, if any, files out to the './disk_rec'
folder, and make use of the clean() function in the main reaPyr script.
After each reaper is run, the clean() function is called, which moves
all carved files in disk_rec to ./harvest/'reaper_name'.  There is
no logic behind this, it was simply a design decision, and I welcome
better formats for who should call 'clean'

* If you'd like to change the recovery directory, change the rec_dir
value in the disk.py class.  Most of the reaper code relies on this
class variable to carve files, write out data, etc...

* Each reaper file, i.e. win_rpr.py, is designed to be run in the same
directory as reaPyr.py.  Many of the file locations are relative, and
based around the reaPyr.py root directory.  As such, if you implement
additional reapers, take note of this fact.

###Installation

reaPyr is designed to run with python 2.7 and the [pytsk3 framework]().
If both of these things are installed and correctly configured, you should
be able to simply pull down this git repo and run
```bash
  $ python reaPyr.py -d <disk image> -o <offset> -s <sector size>
```

####pytsk3

If you are having troubles getting pytsk3 working, here are the steps I followed
for a fresh Ubuntu 13.04 OS.

```bash
  sudo apt-get install build-essential linux-headers-generic libafflib-dev zlib1g-dev libtalloc-dev libtsk3*  
  sudo pip install pytsk3
```

You can verify that pytsk3 installed properly by opening a python interpreter
by typing `python`, and if you can run `import pytsk3` with no errors then everything
should be setup properly.

###Usage

* Below is the detailed usage of reaPyr

```bash
user@system:~$ reaPyr.py [-h] -d DISKNAME [-o OFFSET] [-ss SECTSIZE]

This program carves, or reaps, user credentials from a specified disk image.

optional arguments:
  -h, --help            show this help message and exit
  -d DISKNAME, --diskname DISKNAME
                        Name of the disk image to reap.
  -o OFFSET, --offset OFFSET
                        Offset into disk where OS resides. Default is 0.
  -ss SECTSIZE, --sectsize SECTSIZE
                        Sector size of OS. Default is 512 bytes.
```

* If you are receiving the following stack traces:
```bash
Traceback (most recent call last):
  File "reaPyr.py", line 176, in <module>
    reap(args.diskname, offs, ss)
  File "reaPyr.py", line 109, in reap
    d = disk.Disk(img, offs, ss)
  File "/home/nicholas/School/reaPyr/disk.py", line 50, in __init__
    self.fs = pytsk3.FS_Info(img, offset=self.part_offs*self.sect_size)
IOError: FS_Info_Con: (tsk3.c:189) Unable to open the image as a filesystem: Cannot determine file system type
```
It means that pytsk3 is unable to find the offset for the NTFS partition.
To get reaPyr functioning correctly, run tools such as `fsstat` or `fdisk -l`
to determine what the offset on the disk image is to the root NTFS partition
and then hand this value to reaPyr using the `-o` option.

* The default sector size which reaPyr uses is 512 bytes, however this can
be set using the `-s` option

###Future Work
* Add support for running on multiple OS
* Add reapers for multiple OS

###Author

Nick Anderson - nba237@nyu.edu

###Citations

* Thanks to someone awesome for the baller image of an SC2 Reaper.  Link [here](http://static.giantbomb.com/uploads/original/15/155745/2263839-terran_reaper__starcraft_ii_by_oxoxoxo.jpg)

* [creddump](https://code.google.com/p/creddump/)

* [pytsk3](https://code.google.com/p/pytsk/wiki/pytsk3)



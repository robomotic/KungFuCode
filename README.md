KungFuCode
==========

A gamified version of a code tracking platform.
It is a python daemon task that scan a predefined list of folders
and compute for each file the number of lines of code and the total dimension of the file.
It then computes the density as a measure of productivity and aggregate all the measures 
accross the folder structure.
As a result you can track the volume of code produced for a certain project during time.
The statistics can automagically uploaded on a server (work in progress sorry!) for
later analysis or for comparing other team memembers.
It is compatible with git and svn in the sense that you can ignore files by extension.

Create Doxygen
=============
To create the documentation run:
doxygen config.dox

Dependencies
=============
Python 2.7
SqlAlchemy

Run
=======================
To run it simply do:
python Crawler.py &

logs of activity will be stored in [yourfolder]/logs/daemon.log

To stop it well I don't have an elegant way yet but you can either CTRL+C (safely)
or kill it via ps grep.

Next version will feature an init.RC script to do it properly.


Configuration
==============================
Deploy the code folder somewhere on your Linux home folder.
For example: /home/robomotic/Documents/KungFuCode
Then change the config/parser.ini entry appropriately:

[Installation]
Folder=/home/robomotic/Documents/KungFuCode

Configure the json file on config/folders.json with a list of folders you
want to monitor including what file types you want to index and what file types
you don't want.

The Recursive and Tracking functionality is not implemented yet.
The folder name must be an absolute path otherwise is considered to be a relative path.





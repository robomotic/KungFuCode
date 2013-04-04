# FolderStat: a simple class to recursively scan folders
# Author: Paolo Di Prodi
# Copyright 2012 Robomotic ltd
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#########################################################################
__author__="Paolo Di Prodi"
__version__ = "1.0"
#########################################################################

"""@package FolderStat
This package contains a class for listing files in folders and traversing the file system

"""
import os
import sys
import json
from pprint import pprint
import unittest

class FolderScanner:
    """
    FolderScanner is an utility class to build analytics for folders
    """
    ## a dictionary containing file name -> size
    __fileList = {}
    ## the current file size
    __fileSize=0
    ## the total number of folders
    __folderCount=0
    ## the root folder
    __rootdir = None
    ## json object to contain configuration
    __config=None
    
    def __init__(self, folderPath):
        """The constructor.
        @param folderPath: path to the JSON file containing the folders to be analysed
        """
        ## TODO: should check if the file exists 
        self.LoadSettings(folderPath)
        
    def LoadSettings(self, folderPath):
        """Load settings
        @param folderPath: path to the JSON file containing the folders to be analysed
        """
        json_data=open(folderPath)
        self.__config = json.load(json_data)
        json_data.close()
        
    def GetFileList(self, rootdir, inc, exc):
        """Recursive method to return a file list
        @param rootdir: root folder from where to start
        @param inc: file to be included
        @param exc: file to be excluded
        """
        ### Root directory to begin with
        self.__rootdir=rootdir
        ### walk the root folder 
        for root, subFolders, files in os.walk(rootdir):
            ## scan every file in the folder
            for file in files:
                ## build the full path name
                filename=os.path.join(root,file)
                ## extrapolate the file extension
                filext=os.path.splitext(filename)[1][1:].strip() 
                ## inclusion flag is True
                if inc:
                    if filext in inc:
                        self.__fileList.update({filename:os.path.getsize(filename)})
                ## exclusion flag is True
                elif exc:
                    if filext not in exc:
                        self.__fileList.update({filename:os.path.getsize(filename)})
            ## recursive call and start over again
            for sub in subFolders:
                self.GetFileList(os.path.join(rootdir,sub), inc, exc)
                
    def GetAutoList(self):
        """ Return a file list satisfying the criterias in the configuration json file """
        self.Reset()
        for rootfolder in self.__config['Folders']:
            self.GetFileList(rootfolder['Name'], rootfolder["FileTypes"], rootfolder["Ignores"])
        return self.__fileList
        
    def Reset(self):
        """ Reset all the code metrics """
        self.__fileList = {}
        self.__fileSize = 0
        self.__folderCount = 0
        self.__rootdir = None
        
    def ScanAll(self, rootdir):
        """ Scall all folders and file without any filtering
        @param rootdir: the root folder where to start
        """
        ### reset all the metrics
        self.Reset()
        self.__rootdir=rootdir
        for root, subFolders, files in os.walk(rootdir):
            ## sum the total number of folders
            self.__folderCount += len(subFolders)
            for file in files:
                f = os.path.join(root,file)
                ## sum the total file size
                self.__fileSize += os.path.getsize(f)

    def GetFileSize(self):
        """ Return the total file size after a call to ScanAll """
        return self.__fileSize;
    def GetFolderNumber(self):
        """ Return the total number of folders after a call to ScanAll """
        return self.__folderCount;


class TotalCount(unittest.TestCase):
    """
    Unit test to measure correctness in measuring number of files and folders
    """
    def setUp(self):
        self.configFolders=os.path.join('config', 'folders.jsn')
        self.folder=FolderScanner(self.configFolders)
    def testAll(self):
        """ Test the basic calculations with the test folder     """
        files=self.folder.GetAutoList()
        self.assertEqual(files, {})
        self.folder.Reset()
        self.folder.ScanAll("tests");
        print("Total Size is {0} bytes".format(self.folder. GetFileSize()))
        self.assertEqual(self.folder.GetFileSize(), 5998)
        print "Total Folder count %d"% self.folder.GetFolderNumber()
        self.assertEqual(self.folder.GetFolderNumber(), 2)


def main():
    unittest.main()
    
if __name__ == "__main__":
    """ This should be called only for unit testing """
    main()

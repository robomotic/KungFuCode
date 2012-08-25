# FileReader: a simple class to count the number of line codes in a file
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

import os
import sys
import json
from pprint import pprint

class FolderScanner:
    __fileList = {}
    __fileSize=0
    __folderCount=0
    __rootdir = None
    __config=None
    
    def __init__(self):
        self.LoadSettings()
        
    def LoadSettings(self):
        json_data=open("config/folders.jsn")
        self.__config = json.load(json_data)
        #ignores=data['Ignores']
        #print ignores
        #pprint(data)
        json_data.close()
        
    def GetFileList(self, rootdir, inc, exc):
        self.__rootdir=rootdir
        for root, subFolders, files in os.walk(rootdir):
            for file in files:
                filename=os.path.join(root,file)
                filext=os.path.splitext(filename)[1][1:].strip() 
                if inc:
                    if filext in inc:
                        self.__fileList.update({filename:os.path.getsize(filename)})
                        #print "Adding ", filename,  " with size ", os.path.getsize(filename)
                        #self.__fileList[filename]=os.path.getsize(filename)
                elif exc:
                    if filext not in exc:
                        self.__fileList.update({filename:os.path.getsize(filename)})
            for sub in subFolders:
                self.GetFileList(os.path.join(rootdir,sub), inc, exc)
                
    def GetAutoList(self):
        self.Reset()
        for rootfolder in self.__config['Folders']:
            self.GetFileList(rootfolder['Name'], rootfolder["FileTypes"], rootfolder["Ignores"])
        return self.__fileList
    def Reset(self):
        self.__fileList = {}
        self.__fileSize = 0
        self.__folderCount = 0
        self.__rootdir = None
        
    def ScanAll(self, rootdir):
        self.Reset()
        self.__rootdir=rootdir
        for root, subFolders, files in os.walk(rootdir):
            self.__folderCount += len(subFolders)
            for file in files:
                f = os.path.join(root,file)
                self.__fileSize += os.path.getsize(f)

    def GetFileSize(self):
        return self.__fileSize;
    def GetFolderNumber(self):
        return self.__folderCount;
        
if __name__ == "__main__":
    folder=FolderScanner()
    files=folder.GetFileList("tests")
    print files
    folder.Reset()
    folder.ScanAll("tests");
    print("Total Size is {0} bytes".format(folder. GetFileSize()))
    print "Total Folder count %d"% folder.GetFolderNumber()

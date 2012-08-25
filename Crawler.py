# Crawler: this is the main daemon to compute all the code analytics
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

import time
import logging
from FolderStat import *
from FileStat import  *
from Database import *
import ConfigParser

def log():
    logging.info('Updating database index')
    

class Task(object):
    def __init__(self, func, delay, args=()):
        self.args = args
        self.function = func
        self.delay = delay
        self.next_run = time.time() + self.delay
        logging.basicConfig(filename="daemon.log",level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')        #formatter = UTCFormatter('[%(asctime)s] %(message)s', '%d/%b/%Y:%H:%M:%S')
        #fh.setFormatter(formatter)
        #logging.addHandler(fh) 
        self.folder=FolderScanner()
        self.database=FileIndex()
        self.loadConfig()

    def loadTestConfig(self):
        Config = ConfigParser.ConfigParser()
        Config.read("config/parser.ini")
        self.top=Config.get("TestFolder", "Path")
        self.delay=Config.get("Params", "Frequency")
        self.delay=float(self.delay)
        logging.info('Scanning test folder')
        
    def loadConfig(self):
        Config = ConfigParser.ConfigParser()
        Config.read("config/parser.ini")
        self.delay=Config.get("Params", "Frequency")
        self.delay=float(self.delay)
        logging.info('Scanning test folder')
        
    def compute(self):
        #get the list of files
        #self.list=self.folder.GetFileList(self.top)
        self.list=self.folder.GetAutoList()
        if self.list==None:
            return 0
        else: print self.list
        summary={}
        #compute lines of code and density
        for filepath, size in self.list.items():    
            reader=FileReader(filepath)
            currentLines=reader.GetLines()
            #now add to database
            extension=os.path.splitext(filepath)[1][1:].strip() 
            if extension in summary.keys():
                summary[extension]+=currentLines
            else:
                summary[extension]=currentLines
            self.database.addEntry(filepath, extension,currentLines,  size)
        self.UpdateResults(summary)
        
    def UpdateResults(self, summary):
        print "TODO: update results"
        print summary
    def shouldRun(self):
        return time.time() >= self.next_run

    def run(self):
        self.function(*(self.args))
        self.compute(*(self.args))
        self.next_run += self.delay
        # self.next_run = time.time() + self.delay

if __name__ == "__main__":
    
    tasks = [Task(log,  interval )] 
    while True:
        for t in tasks:
            if t.shouldRun():
                t.run()
            time.sleep(0.01)

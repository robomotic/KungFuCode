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

#########################################################################
__author__="Paolo Di Prodi"
__version__ = "1.0"
#########################################################################

"""@package Crawler
This is the main script for indexing and crawling recurrently the folder specified in the configuration folder.

"""
import time
import logging
import os
import errno
import ConfigParser
from pprint import pprint
## library imports
from utils.FolderStat import FolderScanner
from utils.FileStat import FileReader
from utils.Database import FileIndex
from utils.Communicator import Client

## global variable to keep the current directory
working_dir = os.path.dirname(__file__)

class myLogger(object):
    """
    myLogger is a decorator class for changing the loggin functionality
    """
    def __init__(self, arg1):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        ## Verify print "Inside __init__()"
        self.arg1 = arg1

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        def wrapped_f(*args):
            ## want to call the original one ? -> f(*args)
            logging.info(self.arg1)
        return wrapped_f

@myLogger("Periodic Scan")
def log(message):
    """Notify when database is updated

    Called every often to update the database.
    Default behaviour is to print the message
    """
    print message

def make_sure_path_exists(path):
    """Check if folder exists
    If not creates it
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
            
class Task(object):
    """Task is a generic task for  indexing your folder structure
    Called every often to update the database.
    """
    ## Filename containing the list of folders to scan
    __configFolders=os.path.join('config', 'folders.jsn')
    ## Filename containg the parameters
    __configParams=os.path.join('config', 'parser.ini')

    def __init__(self, func, delay, args=()):
        """The constructor.
        @param func: logger function to be used
        @param delay: how many seconds between each scan
        @args: optional arguments to be passed
        """
        ### List of arguments for functions 
        self.args = args
        ### Any function to be called periodically by the task
        self.function = func
        ### The schedular delay for the background task in seconds
        self.delay = delay
        ### Compute future time of scheduler
        self.next_run = time.time() + self.delay
        ## This is logging everything in the daemon log file with proper timestamps
        ## If you don't need logging just disable it from the myLogger decorator
        make_sure_path_exists('logs')
        logging.basicConfig(filename=os.path.join('logs', 'daemon.log'),
                            level=logging.DEBUG, 
                            format='%(asctime)s %(message)s', 
                            datefmt='%m/%d/%Y %I:%M:%S %p')  
        self.folder=FolderScanner(self.__configFolders)
        self.database=FileIndex()
        self.comm=Client()
        self.loadConfig()

    def loadTestConfig(self):
        """Load a default test folder for Unit Testing
        The configuration should contain a path for TestFolder
        """
        Config = ConfigParser.ConfigParser()
        Config.read(self.__configParams)
        self.top=Config.get("TestFolder", "Path")
        self.delay=Config.get("Params", "Frequency")
        self.delay=float(self.delay)
        logging.info('Scanning test folder ...')
        
    def loadConfig(self):
        """Load a generic test folder
        The configuration contains a rule set for the folder structure
        """
        Config = ConfigParser.ConfigParser()
        Config.read(self.__configParams)
        self.delay=Config.get("Params", "Frequency")
        self.delay=float(self.delay)
        logging.info('Scanning projects ...')
        
    def compute(self):
        """Load a generic test folder
        The configuration contains a rule set for the folder structure
        """
        ## Get the list of files
        self.list=self.folder.GetAutoList()
        if self.list==None:
            return 0
        summary={}
        ## compute lines of code and density
        for filepath, size in self.list.items():    
            reader=FileReader(filepath)
            ## compute the number of new lines in the file
            currentLines=reader.GetLines()
            ## extrapolate the extension from the full file name path
            extension=os.path.splitext(filepath)[1][1:].strip() 
            ## if the extension is the one we want to consider then sum the lines
            if extension in summary.keys():
                summary[extension]+=currentLines
            ## otherwise keep the same number of lines
            else:
                summary[extension]=currentLines
            ## Add the entry into the database containg the full path, the file extension, 
            ## number of lines and size
            self.database.addEntry(filepath, extension,currentLines,  size)
        ## if we want a summary POST the results into the server
        if summary: self.UpdateResults(summary)
        ## log the summary if necessary
        logging.info(''.join(['File with .%s contains %s lines' % (key, value) for (key, value) in summary.items()]))
        
    def UpdateResults(self, summary):
        """Push the code summary on the RESTful server online"""        
        ## TODO: we are not posting anything yet the server is offline
        # self.comm.postStats(summary)
        
    def shouldRun(self):
        """Generic method to verify if the task needs to run
        Check the current time and verify if required run()
        """
        return time.time() >= self.next_run

    def run(self):
        """Task run method
        Call the provided function, compute the code size and schedule the next
        with the provided delay
        """
        self.function(*(self.args))
        self.compute()
        self.next_run += self.delay
        ##TOD: why not this?  self.next_run = time.time() + self.delay

if __name__ == "__main__":
    """Main entry point"""
    ## You can put a list of tasks for simplicity we only require one
    tasks = [Task(log,  5 , args="Periodic Scan")] 
    while True:
        ## scan every task in the list ....
        for t in tasks:
            ## if it has to run then do it otherwise go to the next one!
            if t.shouldRun():
                t.run()
            ## sleep a bit to make the Task responsive in case of a CTRL+C
            time.sleep(0.01)

# Database: this is the part that stores the code  analytics on the local database
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

from sqlalchemy import *
import datetime
import os.path

#########################################################################
__author__="Paolo Di Prodi"
__version__ = "1.0"
#########################################################################

"""@package Communicator
This is the class that is responsible for pushing/pulling data from the RESTful database

"""

def now():
    """Get the local date time"""
    return datetime.datetime.now()

class FileIndex:
    """This is a database class for storing the code metrics on an sqlite file database
    """
    ## database connection object
    __db=None
    ## database name
    __db_name=None
    __metadata=None
    __file_index=None
    ## default path for the database is hidden to prevent accidental manipulation
    __file_path='.db/info.db'
    def __init__(self):
        """The constructor.
        Check if the db file exists.
        If it does establish a connection if not creates it
        """
        ## check first if database was there
        present=os.path.exists(self.__file_path)
        self.__db= create_engine('sqlite:///.db/info.db')
        ## self.__db.echo = False 
        self.__metadata= MetaData(self.__db)
        self.__tables=self.__metadata.tables.keys()
        ## TODO tables are not listed because of a bug in SQL Alchemy needs a workaround
        for t in self.__metadata.sorted_tables:
            print t.name
        ## if database was already full
        if present: self.AutoLoad()
        else: self.InitIndex()
        
    def AutoLoad(self):
        """Load the index table if present already"""
        self.__file_index=Table('index', self.__metadata, autoload=True)
        
    def InitIndex(self):
        """Initialize the index table"""
        self.__file_index = Table('index', self.__metadata,
            Column('file_id', Integer, primary_key=True),
            ## full pathname of the file
            Column('filename', String),
            ## md5 of the filename to verify if it was changed
            Column('hash', String),
            ## number of new lines in the file
            Column('rows', Integer),
            ## number of bytes
            Column('size', Integer), 
            ## file name extension
            Column('ext', String),
           ## when the file was scanned the last time 
            Column('time',  TIMESTAMP(), default=now())
        )
        ## create the table structure for the index
        self.__file_index.create()
        ## create a table with the full filename to normalize the database
        self.__file_name=Table('file', self.__metadata,
            Column('filename', String, primary_key=True),
            Column('file_id', Integer, ForeignKey('index.file_id')),
        )
        self.__file_name.create()

    def addEntry(self, filepath, ext, rows, size):
        """Add an entry in the database"""
        operation = self.__file_index.insert()
        result=operation.execute(filename=filepath, hash='None', rows=rows, size=size, time=now(), ext=ext)
        
    def getAll(self):
        """Print out all the entries for debugging purposes"""
        operation = self.__file_index.select()
        result = operation.execute()
        row = result.fetchone()
        for row in result:
            print row
            
        
class FileEntry(object):
    pass
    
class DirectoryEntry(object):
    pass
if __name__ == "__main__":
    indexer=FileIndex()
    #indexer.addEntry("pippo.c", 1232,  1232L)
    indexer.getAll()

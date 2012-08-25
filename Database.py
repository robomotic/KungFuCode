from sqlalchemy import *
import datetime
import os.path

def now():
    return datetime.datetime.now()

class FileIndex:
    __db=None
    __db_name=None
    __metadata=None
    __file_index=None
    __file_path='.db/info.db'
    def __init__(self):
        #check first if database was there
        present=os.path.exists(self.__file_path)
        self.__db= create_engine('sqlite:///.db/info.db')
        #self.__db.echo = False 
        self.__metadata= MetaData(self.__db)
        self.__tables=self.__metadata.tables.keys()
        #TODO tables are not listed because of a bug in SQL Alchemy needs a workaround
        for t in self.__metadata.sorted_tables:
            print t.name
        #if database was already full
        if present: self.AutoLoad()
        else: self.InitIndex()
    def AutoLoad(self):
        self.__file_index=Table('index', self.__metadata, autoload=True)
    def InitIndex(self):
        self.__file_index = Table('index', self.__metadata,
            Column('file_id', Integer, primary_key=True),
            Column('filename', String),
            Column('hash', String),
            Column('rows', Integer),
            Column('size', Integer), 
            Column('ext', String), 
            Column('time',  TIMESTAMP(), default=now())
        )
        self.__file_index.create()
        #see code here http://stackoverflow.com/questions/414952/sqlalchemy-datetime-timezone
    def addEntry(self, filepath, ext, rows, size):
        operation = self.__file_index.insert()
        result=operation.execute(filename=filepath, hash='None', rows=rows, size=size, time=now(), ext=ext)
        
    def getAll(self):
        operation = self.__file_index.select()
        result = operation.execute()
        row = result.fetchone()
        for row in result:
            print row
            
    def now(self):
        return datetime.datetime.now()
        
class FileEntry(object):
    pass
    
class DirectoryEntry(object):
    pass
if __name__ == "__main__":
    indexer=FileIndex()
    #indexer.addEntry("pippo.c", 1232,  1232L)
    indexer.getAll()
